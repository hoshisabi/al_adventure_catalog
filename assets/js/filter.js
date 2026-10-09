// Lean Catalog Filter Logic (Client-Side)

// State
let catalog = [];       // All adventure objects
let filteredItems = []; // Subset after filters
let currentPage = 1;
let itemsPerPage = 48;

let filters = {
    campaign: '',
    season: '',
    tier: '',
    hours: '',
    source: '',
    ccOnly: false,
    hideAiContent: false,
    privateOnly: false,
    showProductId: false,
    showAuthor: false,
    search: '',
    inventoryURL: '',
    privateLinks: {}
};

let sortBy = 'date-desc';
let viewMode = 'grid';
let highlightedAdventureId = null;

const CAMPAIGN_MAP = {
    1: 'Forgotten Realms',
    2: 'Eberron',
    4: 'Ravenloft',
    8: 'Dragonlance',
    16: 'Critical Role',
};

// Config
const baseURL = 'assets/data/';

// Escape text for use in HTML element content or a quoted attribute value.
function escapeHtml(val) {
    return String(val ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Return the URL only if it is an absolute http(s) URL; anything else
// (javascript:, data:, relative paths) returns null. Private inventory links
// can come from an arbitrary ?inventory= URL, so they must not be trusted as hrefs.
function safeUrl(url) {
    if (typeof url !== 'string') return null;
    try {
        const parsed = new URL(url);
        return (parsed.protocol === 'http:' || parsed.protocol === 'https:') ? parsed.href : null;
    } catch {
        return null;
    }
}

function getPrivateLink(adv) {
    const productId = String(adv.i).replace(/-\d+$/, '');
    return safeUrl(filters.privateLinks[adv.i] || filters.privateLinks[productId]);
}

// Initialization
async function initialize() {
    console.log('Initializing Lean Catalog...');

    try {
        // Handle Private Inventory before or during catalog load
        await loadPrivateInventory();

        // Use a simple fetch. Browsers will use ETag/Last-Modified headers 
        // to check if catalog.json has changed without re-downloading the whole file
        // if the server (GitHub Pages) says it hasn't changed (304 Not Modified).
        const resp = await fetch(`${baseURL}catalog.json`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();

        if (data.adventures && Array.isArray(data.adventures)) {
            catalog = data.adventures;
            if (data.last_update) {
                const lu = data.last_update;
                const formattedDate = `${lu.substring(0, 4)}-${lu.substring(4, 6)}-${lu.substring(6, 8)}`;
                const luContainer = document.getElementById('last-update-container');
                const luDate = document.getElementById('last-update-date');
                if (luContainer && luDate) {
                    luDate.innerHTML = `<a href="https://github.com/hoshisabi/al_adventure_catalog/commits/main" target="_blank" class="hover:underline">${escapeHtml(formattedDate)}</a>`;
                    luContainer.classList.remove('hidden');
                }
            }
        } else {
            catalog = data;
        }

        console.log(`Loaded ${catalog.length} adventures.`);

        // Populate Dropdowns from Data
        populateFilterUI();

        // Initial Display
        filteredItems = [...catalog]; // Default: no filter
        updateItemsPerPage();
        setupEventListeners();
        updateViewToggleButtons();

        // Apply filters from URL if present, then run filter logic
        applyFiltersFromURL();

    } catch (err) {
        console.error('Failed to initialize:', err);
        document.getElementById('results').innerHTML = `<p class="p-4 text-red-600">Error loading catalog: ${escapeHtml(err.message)}</p>`;
    }
}

async function loadPrivateInventory() {
    const params = new URLSearchParams(window.location.search);
    let invURL = params.get('inventory');

    // Check URL param
    if (invURL) {
        filters.inventoryURL = invURL;
        try {
            console.log('Fetching private inventory from:', invURL);
            const resp = await fetch(invURL);
            if (resp.ok) {
                filters.privateLinks = await resp.json();
                console.log(`Loaded ${Object.keys(filters.privateLinks).length} private links from URL.`);
            }
        } catch (e) {
            console.warn('Failed to load private inventory:', e);
        }
    }

    // Load from Local Storage and Merge
    try {
        const localRaw = localStorage.getItem('private_inventory');
        if (localRaw) {
            const localData = JSON.parse(localRaw);
            // Merge: local overwrites remote if there's a conflict
            filters.privateLinks = { ...filters.privateLinks, ...localData };
            console.log(`Merged ${Object.keys(localData).length} items from Local Storage.`);
        }
    } catch (e) {
        console.warn('Failed to load private inventory from Local Storage:', e);
    }
}

function updateItemsPerPage() {
    if (window.innerWidth >= 992) {
        itemsPerPage = 48;
    } else {
        itemsPerPage = 24;
    }
    // Logic mostly handled in displayResults, but nice to reset page
    currentPage = 1;
    displayResults();
}

function populateFilterUI() {
    // 1. Campaigns (p)
    // p is now a bitmask (integer)
    const allCampaigns = new Set();
    catalog.forEach(adv => {
        if (typeof adv.p === 'number') {
            for (const [bit, name] of Object.entries(CAMPAIGN_MAP)) {
                if (adv.p & parseInt(bit)) allCampaigns.add(name);
            }
        } else if (Array.isArray(adv.p)) {
            adv.p.forEach(c => allCampaigns.add(c));
        } else if (adv.p) {
            allCampaigns.add(adv.p);
        }
    });
    const sortedCampaigns = Array.from(allCampaigns).sort();
    populateDropdown('campaign', sortedCampaigns, 'All Campaigns');

    // 2. Tiers (t)
    const allTiers = new Set();
    catalog.forEach(adv => {
        if (adv.t !== null && adv.t !== undefined) allTiers.add(Number(adv.t));
    });
    const sortedTiers = Array.from(allTiers).sort((a, b) => Number(a) - Number(b));
    populateDropdown('tier', sortedTiers, 'All Tiers');

    // 3. Hours (h)
    // Integers only
    const allHours = new Set();
    catalog.forEach(adv => {
        const h = adv.h;
        if (h) {
            const matches = String(h).match(/\d+/g);
            if (matches) {
                matches.forEach(m => allHours.add(parseInt(m)));
            }
        }
    });
    const sortedHours = Array.from(allHours).sort((a, b) => a - b);
    populateDropdown('hours', sortedHours, 'All Lengths');

    // 4. Seasons (s) — backend (aggregator) normalizes synonyms to one canonical per season
    const allSeasons = new Set();
    catalog.forEach(adv => {
        if (adv.s) allSeasons.add(adv.s);
    });
    const sortedSeasons = Array.from(allSeasons).sort((a, b) => {
        // Extract leading number for sort (e.g., "1 - Name" -> 1)
        const getNum = (s) => {
            const match = String(s).match(/^(\d+)/);
            return match ? parseInt(match[1]) : 999;
        };
        const nA = getNum(a);
        const nB = getNum(b);

        if (nA !== nB) return nA - nB;

        return String(a).localeCompare(String(b));
    });
    populateDropdown('season', sortedSeasons, 'All Seasons');
}

function applyFiltersFromURL() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('campaign')) filters.campaign = params.get('campaign');
    if (params.has('season')) filters.season = params.get('season');
    if (params.has('tier')) filters.tier = params.get('tier');
    if (params.has('hours')) filters.hours = params.get('hours');
    if (params.has('source')) filters.source = params.get('source');
    if (params.has('search')) filters.search = params.get('search');
    if (params.has('ccOnly')) filters.ccOnly = params.get('ccOnly') === 'true';
    if (params.has('hideAi')) filters.hideAiContent = params.get('hideAi') === 'true';
    else if (params.get('aiContent') === 'hide') filters.hideAiContent = true;
    if (params.has('privateOnly')) filters.privateOnly = params.get('privateOnly') === 'true';
    if (params.has('showProductId')) filters.showProductId = params.get('showProductId') === 'true';
    if (params.has('showAuthor')) filters.showAuthor = params.get('showAuthor') === 'true';
    if (params.has('sort')) sortBy = params.get('sort');
    if (params.get('view') === 'card') viewMode = 'card';
    updateViewToggleButtons();

    // Sync to DOM so dropdowns and search input show the URL state
    const campaignEl = document.getElementById('campaign');
    if (campaignEl) campaignEl.value = filters.campaign || '';
    const seasonEl = document.getElementById('season');
    if (seasonEl) seasonEl.value = filters.season || '';
    const tierEl = document.getElementById('tier');
    if (tierEl) tierEl.value = filters.tier || '';
    const hoursEl = document.getElementById('hours');
    if (hoursEl) hoursEl.value = filters.hours || '';
    const sourceEl = document.getElementById('source');
    if (sourceEl) sourceEl.value = filters.source || '';
    const sortEl = document.getElementById('sort');
    if (sortEl) sortEl.value = sortBy || 'date-desc';
    const searchEl = document.getElementById('search');
    if (searchEl) searchEl.value = filters.search || '';

    const ccOnlyEl = document.getElementById('cc-only');
    if (ccOnlyEl) ccOnlyEl.checked = filters.ccOnly || false;
    const hideAiEl = document.getElementById('hide-ai-content');
    if (hideAiEl) hideAiEl.checked = filters.hideAiContent || false;
    const privateOnlyEl = document.getElementById('private-only');
    if (privateOnlyEl) privateOnlyEl.checked = filters.privateOnly || false;
    const showProductIdEl = document.getElementById('show-product-id');
    if (showProductIdEl) showProductIdEl.checked = filters.showProductId || false;
    const showAuthorEl = document.getElementById('show-author');
    if (showAuthorEl) showAuthorEl.checked = filters.showAuthor || false;

    applyFilters();
}

function updateURLFromFilters() {
    const params = new URLSearchParams();
    if (filters.campaign) params.set('campaign', filters.campaign);
    if (filters.season) params.set('season', filters.season);
    if (filters.tier) params.set('tier', filters.tier);
    if (filters.hours) params.set('hours', filters.hours);
    if (filters.source) params.set('source', filters.source);
    if (filters.search) params.set('search', filters.search);
    if (filters.ccOnly) params.set('ccOnly', 'true');
    if (filters.hideAiContent) params.set('hideAi', 'true');
    if (filters.privateOnly) params.set('privateOnly', 'true');
    if (filters.showProductId) params.set('showProductId', 'true');
    if (filters.showAuthor) params.set('showAuthor', 'true');
    if (sortBy && sortBy !== 'date-desc') params.set('sort', sortBy);
    if (viewMode !== 'grid') params.set('view', viewMode);

    const query = params.toString();
    const newUrl = window.location.pathname + (query ? '?' + query : '') + (window.location.hash || '');
    history.replaceState(null, '', newUrl);
}

function populateDropdown(id, values, defaultText) {
    const select = document.getElementById(id);
    if (!select) return;
    select.innerHTML = '';
    const def = document.createElement('option');
    def.value = '';
    def.textContent = defaultText;
    select.appendChild(def);
    values.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        select.appendChild(opt);
    });
}

function getAdventureSource(adv) {
    const u = adv.u;
    if (u) {
        if (u.includes('dndbeyond.com')) return 'dndbeyond';
        if (u.includes('dmsguild.com')) return 'dmsguild';
        return 'none';
    }
    // No stored URL: only numeric product IDs can derive a DM's Guild link.
    const cleanProductId = String(adv.i).replace(/-\d+$/, '');
    if (/^\d+$/.test(cleanProductId)) return 'dmsguild';
    return 'none';
}

const AFFILIATE_ID = '171040';

// Build the outbound link for an adventure. The affiliate ID is not stored in
// catalog.json (to save space); it's appended here, and only for DM's Guild
// links, since other storefronts (e.g. D&D Beyond) reject the extra param.
// Returns null when no purchasable/viewable URL exists (e.g. print-only
// promotional adventures), so callers can render the title as plain text.
function resolveUrl(adventure) {
    const cleanProductId = String(adventure.i).replace(/-\d+$/, '');
    let url = adventure.u;
    if (!url) {
        // Only fall back to a DM's Guild product page for real (numeric)
        // DM's Guild product IDs. Non-numeric IDs (e.g. D&D Beyond entries
        // with no stored URL) have no derivable link.
        if (!/^\d+$/.test(cleanProductId)) return null;
        url = `https://www.dmsguild.com/product/${cleanProductId}/`;
    }
    if (url.includes('dmsguild.com') && !url.includes('affiliate_id=')) {
        url += (url.includes('?') ? '&' : '?') + `affiliate_id=${AFFILIATE_ID}`;
    }
    return url;
}

// Logic
function applyFilters() {
    console.time('Apply Filters');

    // 0. Base List
    let results = [...catalog];

    // 1. Filter
    // ... filters ...
    if (filters.campaign) {
        results = results.filter(adv => {
            if (typeof adv.p === 'number') {
                const bit = Object.keys(CAMPAIGN_MAP).find(k => CAMPAIGN_MAP[k] === filters.campaign);
                return bit && (adv.p & parseInt(bit));
            }
            const c = adv.p;
            return (Array.isArray(c) && c.includes(filters.campaign)) || c === filters.campaign;
        });
    }

    if (filters.tier) {
        results = results.filter(adv => String(adv.t) === filters.tier);
    }

    if (filters.hours) {
        const target = parseInt(filters.hours);
        results = results.filter(adv => {
            if (!adv.h) return false;
            const hStr = String(adv.h);
            // Range check
            const rangeMatch = hStr.match(/(\d+)\s*-\s*(\d+)/);
            if (rangeMatch) {
                const s = parseInt(rangeMatch[1]);
                const e = parseInt(rangeMatch[2]);
                return target >= s && target <= e;
            }
            // Single check
            const singleMatch = hStr.match(/(\d+)/);
            if (singleMatch) {
                return parseInt(singleMatch[1]) === target;
            }
            return false;
        });
    }

    if (filters.season) {
        results = results.filter(adv => adv.s && String(adv.s) === filters.season);
    }

    if (filters.privateOnly) {
        results = results.filter(adv => getPrivateLink(adv));
    }

    if (filters.ccOnly) {
        results = results.filter(adv => adv.f && (adv.f & 1));
    }

    if (filters.hideAiContent) {
        results = results.filter(adv => adv.ac !== 2);
    }

    if (filters.source) {
        results = results.filter(adv => getAdventureSource(adv) === filters.source);
    }

    if (filters.search) {
        const q = filters.search.toLowerCase();
        results = results.filter(adv => {
            const authors = Array.isArray(adv.a) ? adv.a.join(' ').toLowerCase() : (adv.a || '').toLowerCase();
            return (adv.n && adv.n.toLowerCase().includes(q)) ||
                (adv.c && adv.c.toLowerCase().includes(q)) ||
                authors.includes(q);
        });
    }

    // 2. Sort
    let field, dir;
    if (sortBy) {
        [field, dir] = sortBy.split('-');
    } else {
        field = 'date';
        dir = 'desc';
    }

    results.sort((a, b) => {
        let valA, valB;

        if (field === 'date') {
            valA = a.d || '00000000';
            valB = b.d || '00000000';
        } else if (field === 'title') {
            valA = (a.n || '').toLowerCase();
            valB = (b.n || '').toLowerCase();
        } else if (field === 'code') {
            valA = (a.c || '').toLowerCase();
            valB = (b.c || '').toLowerCase();
        } else if (field === 'id') {
            // Sort by numerical ID; non-numeric IDs (e.g. DnD Beyond "SRC-00125") sort last
            const cleanId = (i) => {
                const n = parseInt(String(i).split('-')[0]);
                return isNaN(n) ? Number.MAX_SAFE_INTEGER : n;
            };
            valA = cleanId(a.i);
            valB = cleanId(b.i);
        } else if (field === 'tier') {
            valA = (a.t !== null && a.t !== undefined) ? Number(a.t) : -1;
            valB = (b.t !== null && b.t !== undefined) ? Number(b.t) : -1;
        } else if (field === 'hours') {
            // Average hours? Or just start?
            // Format: "4", "2-4" -> take first number
            const getH = (h) => {
                if (!h) return 0;
                if (Array.isArray(h)) return parseInt(h[0]) || 0;
                return parseInt(String(h).match(/\d+/)) || 0;
            };
            valA = getH(a.h);
            valB = getH(b.h);
        } else if (field === 'campaign') {
            // Sort by campaign name
            valA = formatCampaigns(a.p).toLowerCase();
            valB = formatCampaigns(b.p).toLowerCase();
        } else if (field === 'author') {
            valA = (formatList(a.a) || '').toLowerCase();
            valB = (formatList(b.a) || '').toLowerCase();
        }

        if (valA < valB) return dir === 'asc' ? -1 : 1;
        if (valA > valB) return dir === 'asc' ? 1 : -1;

        // Secondary sort by title if dates/codes are equal
        if (field !== 'title') {
            let titleA = (a.n || '').toLowerCase();
            let titleB = (b.n || '').toLowerCase();
            if (titleA < titleB) return -1;
            if (titleA > titleB) return 1;
        }
        return 0;
    });

    filteredItems = results;
    console.timeEnd('Apply Filters');
    console.log(`Filtered to ${filteredItems.length} items`);

    currentPage = 1;
    displayResults();
    updateFilterToggleLabel();
    renderActiveFilters();
}

function displayResults() {
    const resultsDiv = document.getElementById('results');
    if (!resultsDiv) return;

    // Counts
    const total = filteredItems.length;
    const start = (currentPage - 1) * itemsPerPage;
    const end = Math.min(start + itemsPerPage, total);

    document.getElementById('showing-start').textContent = total > 0 ? start + 1 : 0;
    document.getElementById('showing-end').textContent = end;
    document.getElementById('total-results').textContent = total;

    // Bottom Stats
    const ssb = document.getElementById('showing-start-bottom');
    if (ssb) ssb.textContent = total > 0 ? start + 1 : 0;
    const seb = document.getElementById('showing-end-bottom');
    if (seb) seb.textContent = end;
    const trb = document.getElementById('total-results-bottom');
    if (trb) trb.textContent = total;

    updatePaginationUI();

    // Render
    const pageItems = filteredItems.slice(start, end);
    resultsDiv.innerHTML = '';

    if (total === 0) {
        resultsDiv.className = 'results-empty';
        resultsDiv.innerHTML = catalog.length
            ? '<p>No adventures match these filters.</p><button type="button" id="empty-clear-filters">Clear filters</button>'
            : '<p>No adventures loaded.</p>';
        document.getElementById('empty-clear-filters')?.addEventListener('click', clearFilters);
        return;
    }

    if (viewMode === 'grid') {
        resultsDiv.className = 'overflow-x-auto';
        renderGridView(pageItems, resultsDiv);
    } else {
        resultsDiv.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';
        pageItems.forEach(adv => {
            resultsDiv.appendChild(createCard(adv));
        });

        // After cards are rendered, check for highlight
        if (highlightedAdventureId) {
            const card = document.getElementById(`card-${highlightedAdventureId}`);
            if (card) {
                // Scroll to the card and move keyboard focus to it
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.tabIndex = -1;
                card.focus({ preventScroll: true });

                card.classList.add('card-highlight');

                // Clear after timeout
                setTimeout(() => {
                    card.classList.remove('card-highlight');
                    highlightedAdventureId = null;
                }, 3000);
            } else {
                // If not found (maybe on another page), clear it
                highlightedAdventureId = null;
            }
        }
    }
}

// ... Rendering functions (Card/Grid) ...

// Scroll the active-filter chips into view if they're off-screen, so a filter
// added from inside the results is visible without opening the filter panel.
function revealActiveFilters() {
    const chips = document.getElementById('active-filters');
    if (!chips) return;
    const top = chips.getBoundingClientRect().top;
    if (top < 0 || top > window.innerHeight) {
        chips.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function setHideAiContent(hide, { reveal = false } = {}) {
    filters.hideAiContent = hide;
    const hideAiEl = document.getElementById('hide-ai-content');
    if (hideAiEl) hideAiEl.checked = hide;

    applyFilters();
    updateURLFromFilters();
    if (reveal) revealActiveFilters();
}

// Called from pills/links inside the results: adds the filter as a chip
function filterByValue(field, value) {
    if (field === 'author' || field === 'search') {
        filters.search = value;
        const searchEl = document.getElementById('search');
        if (searchEl) searchEl.value = value;
    } else {
        filters[field] = value;
        const el = document.getElementById(field);
        if (el) el.value = value;
    }

    applyFilters();
    updateURLFromFilters();
    revealActiveFilters();
}

function makeFilterChip(field, value, displayText) {
    const escaped = escapeHtml(value);
    const label = escapeHtml(displayText !== undefined ? displayText : value);
    return `<span class="filter-chip cursor-pointer text-blue-600 hover:underline hover:text-blue-800" data-filter="${field}" data-value="${escaped}" title="Filter by: ${label}">${label}</span>`;
}

function makeCampaignChips(p) {
    const names = [];
    if (typeof p === 'number') {
        for (const [bit, name] of Object.entries(CAMPAIGN_MAP)) {
            if (p & parseInt(bit)) names.push(name);
        }
    } else if (Array.isArray(p)) {
        names.push(...p.filter(x => x));
    } else if (p) {
        names.push(p);
    }
    if (names.length === 0) return '<span>Unspecified</span>';
    return names.map(n => makeFilterChip('campaign', n)).join(', ');
}

function makeAuthorChips(a) {
    const items = Array.isArray(a) ? a.filter(x => x) : (a ? [a] : []);
    if (items.length === 0) return '<span>N/A</span>';
    return items.map(name => makeFilterChip('author', name)).join(', ');
}

function makeSeasonChip(s) {
    if (!s) return '<span>Unspecified</span>';
    return makeFilterChip('season', s);
}

function makeTierChip(t) {
    if (t === null || t === undefined) return '<span>Unspecified</span>';
    return makeFilterChip('tier', String(t));
}

function makeHoursChip(h) {
    if (!h) return '<span>Unspecified</span>';
    const display = formatHours(h);
    const firstNum = String(h).match(/\d+/);
    if (!firstNum) return `<span>${escapeHtml(display)}</span>`;
    return makeFilterChip('hours', firstNum[0], display);
}

function tierPill(t) {
    if (t === null || t === undefined) return '';
    return `<span class="meta-pill tier-${t} filter-chip" data-filter="tier" data-value="${t}" title="Filter: Tier ${t}">Tier ${t}</span>`;
}

function hoursPill(h) {
    if (!h) return '';
    const display = escapeHtml(formatHours(h));
    const firstNum = String(h).match(/\d+/);
    if (!firstNum) return `<span class="meta-pill">${display}</span>`;
    const n = parseInt(firstNum[0]);
    const colorClass = [1, 2, 4, 8].includes(n) ? `hours-${n}` : 'hours-other';
    return `<span class="meta-pill ${colorClass} filter-chip" data-filter="hours" data-value="${firstNum[0]}" title="Filter by hours">${display}</span>`;
}

function seasonPill(s) {
    if (!s) return '';
    const escaped = escapeHtml(s);
    return `<span class="meta-pill clickable filter-chip" data-filter="season" data-value="${escaped}" title="Filter by season">${escaped}</span>`;
}

function aiPill(ac) {
    if (ac !== 2) return '';
    return `<span class="meta-pill ai-assisted clickable filter-chip" data-filter="hide-ai" title="Hide AI assisted content (publisher self-disclosure on DM's Guild)">AI assisted</span>`;
}

function datePill(d) {
    if (!d) return '';
    const s = String(d);
    const formatted = `${s.substring(0, 4)}-${s.substring(4, 6)}-${s.substring(6, 8)}`;
    return `<span class="meta-pill">${escapeHtml(formatted)}</span>`;
}

function campaignPills(p) {
    const names = [];
    if (typeof p === 'number') {
        for (const [bit, name] of Object.entries(CAMPAIGN_MAP)) {
            if (p & parseInt(bit)) names.push(name);
        }
    } else if (Array.isArray(p)) {
        names.push(...p.filter(x => x));
    } else if (p) {
        names.push(p);
    }
    return names.map(n => {
        const escaped = escapeHtml(n);
        return `<span class="meta-pill clickable filter-chip" data-filter="campaign" data-value="${escaped}" title="Filter: ${escaped}">${escaped}</span>`;
    }).join('');
}

function makeCodeChip(c) {
    if (!c) return '<span>N/A</span>';
    const series = c.replace(/[^a-zA-Z]*\d+$/, '') || c;
    const escaped = escapeHtml(series);
    return `<span class="filter-chip cursor-pointer text-blue-600 hover:underline hover:text-blue-800" data-filter="search" data-value="${escaped}" title="Filter by series: ${escaped}">${escapeHtml(c)}</span>`;
}

function createCard(adventure) {
    const card = document.createElement('div');
    card.id = `card-${adventure.i}`;
    card.className = 'border rounded-xl p-4 shadow-lg hover:shadow-xl transition-all bg-white';

    const url = safeUrl(resolveUrl(adventure));
    const privateLink = getPrivateLink(adventure);
    const title = escapeHtml(adventure.n || 'Untitled');

    card.innerHTML = `
        <div class="flex justify-between items-start mb-2">
            ${url
                ? `<a href="${escapeHtml(url)}" target="_blank" class="text-lg font-semibold text-blue-600 hover:text-blue-800 block leading-snug">
                ${title}
            </a>`
                : `<span class="text-lg font-semibold block leading-snug" style="color:var(--text)" title="No public link available">
                ${title}
            </span>`}
            ${privateLink ? `
                <a href="${escapeHtml(privateLink)}" target="_blank" rel="noopener noreferrer" title="View Private PDF" class="ml-2 p-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                    </svg>
                </a>
            ` : ''}
        </div>
        ${filters.showProductId ? `<p class="text-xs text-gray-400 mb-1"><span class="font-medium">Product ID:</span> ${escapeHtml(adventure.i)}</p>` : ''}
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Code:</span> ${makeCodeChip(adventure.c)}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Author(s):</span> ${makeAuthorChips(adventure.a)}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Campaign:</span> ${makeCampaignChips(adventure.p)}</p>
        <div class="card-meta">
            ${tierPill(adventure.t)}
            ${hoursPill(adventure.h)}
            ${seasonPill(adventure.s)}
            ${aiPill(adventure.ac)}
            ${datePill(adventure.d)}
        </div>
    `;

    card.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', e => {
            e.stopPropagation();
            if (chip.dataset.filter === 'hide-ai') {
                setHideAiContent(true, { reveal: true });
                return;
            }
            filterByValue(chip.dataset.filter, chip.dataset.value);
        });
    });

    return card;
}

function renderGridView(adventures, container) {
    const table = document.createElement('table');
    table.className = 'w-full border-collapse bg-white';

    const showProductId = filters.showProductId;
    const showAuthor = filters.showAuthor;

    const header = (col, label, extraClass = 'whitespace-nowrap') => {
        const active = sortBy.startsWith(col + '-');
        const asc = sortBy.endsWith('asc');
        const ariaSort = active ? (asc ? 'ascending' : 'descending') : 'none';
        const icon = active ? (asc ? '↑' : '↓') : '↕';
        return `<th class="text-left border ${extraClass} ${active ? 'bg-gray-200' : ''}" data-sort="${col}" aria-sort="${ariaSort}">
            <button type="button" class="sort-header px-4 py-2">${label} <span class="ml-1" aria-hidden="true">${icon}</span></button>
        </th>`;
    };

    table.innerHTML = `
        <thead class="bg-gray-100 text-xs uppercase text-gray-700">
            <tr>
                ${showProductId ? header('id', 'ID') : ''}
                ${header('code', 'Code')}
                ${header('title', 'Title', 'min-w-[10rem]')}
                ${showAuthor ? header('author', 'Author') : ''}
                ${header('tier', 'Tier')}
                ${header('hours', 'Hours')}
                ${header('campaign', 'Campaign')}
                ${header('date', 'Added')}
            </tr>
        </thead>
        <tbody></tbody>
    `;

    table.querySelectorAll('th[data-sort] button').forEach(btn => {
        btn.addEventListener('click', () => {
            const col = btn.closest('th').dataset.sort;
            const newDir = (sortBy.startsWith(col + '-') && sortBy.endsWith('asc')) ? 'desc' : 'asc';
            sortBy = `${col}-${newDir}`;

            // Keep the dropdown in sync when it has a matching option
            const sortDropdown = document.getElementById('sort');
            if (sortDropdown?.querySelector(`option[value="${sortBy}"]`)) {
                sortDropdown.value = sortBy;
            }

            applyFilters();
            updateURLFromFilters();
            // The table was rebuilt; return focus to the same header
            document.querySelector(`#results th[data-sort="${col}"] button`)?.focus();
        });
    });

    const tbody = table.querySelector('tbody');
    adventures.forEach(adv => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50 cursor-pointer transition-colors';
        // Rows open the adventure in card view; tabindex + Enter/Space make that keyboard-reachable
        row.tabIndex = 0;
        const openAsCard = () => {
            highlightedAdventureId = adv.i;
            setViewMode('card');
        };
        row.addEventListener('click', (e) => {
            // If we click an anchor, don't trigger the view switch
            if (e.target.closest('a')) return;
            openAsCard();
        });
        row.addEventListener('keydown', (e) => {
            if (e.target !== row || (e.key !== 'Enter' && e.key !== ' ')) return;
            e.preventDefault();
            openAsCard();
        });
        const dateAdded = adv.d ? (s => `${s.substring(0, 4)}-${s.substring(4, 6)}-${s.substring(6, 8)}`)(String(adv.d)) : '';
        const cleanProductId = String(adv.i).replace(/-\d+$/, '');
        const url = safeUrl(resolveUrl(adv));
        const privateLink = getPrivateLink(adv);
        const title = escapeHtml(adv.n);

        row.innerHTML = `
             ${showProductId ? `<td class="px-4 py-2 border text-sm whitespace-nowrap">${escapeHtml(cleanProductId)}</td>` : ''}
             <td class="px-4 py-2 border whitespace-nowrap">${escapeHtml(adv.c)}</td>
             <td class="px-4 py-2 border">
                <div class="flex items-center justify-between">
                    ${url
                        ? `<a href="${escapeHtml(url)}" target="_blank" class="text-blue-600 hover:underline">${title}</a>`
                        : `<span style="color:var(--text)" title="No public link available">${title}</span>`}
                    ${privateLink ? `
                        <a href="${escapeHtml(privateLink)}" target="_blank" rel="noopener noreferrer" class="ml-2 text-green-600 hover:text-green-800" title="Private PDF">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                            </svg>
                        </a>
                    ` : ''}
                </div>
             </td>
             ${showAuthor ? `<td class="px-4 py-2 border text-sm">${escapeHtml(formatList(adv.a))}</td>` : ''}
             <td class="px-4 py-2 border whitespace-nowrap">${adv.t != null ? escapeHtml(adv.t) : '-'}</td>
             <td class="px-4 py-2 border whitespace-nowrap">${escapeHtml(formatHours(adv.h))}</td>
             <td class="px-4 py-2 border whitespace-nowrap">${formatCampaignsTable(adv.p)}</td>
             <td class="px-4 py-2 border text-sm text-gray-500 italic whitespace-nowrap">${dateAdded}</td>
        `;
        tbody.appendChild(row);
    });

    container.appendChild(table);
}

function formatList(val) {
    if (Array.isArray(val)) return val.filter(x => x).join(', ');
    return val;
}

function formatCampaigns(p) {
    if (typeof p === 'number') {
        const names = [];
        for (const [bit, name] of Object.entries(CAMPAIGN_MAP)) {
            if (p & parseInt(bit)) names.push(name);
        }
        return names.join(', ');
    }
    return formatList(p);
}

function formatHours(val) {
    if (!val) return '-';
    if (Array.isArray(val)) return val.join(', ') + ' hr';
    return val + ' hr';
}

const CAMPAIGN_ABBREV = { 1: 'FR', 2: 'EB', 4: 'RL', 8: 'DL', 16: 'CR' };

function formatCampaignsTable(p) {
    if (typeof p === 'number') {
        const parts = [];
        for (const [bit, name] of Object.entries(CAMPAIGN_MAP)) {
            if (p & parseInt(bit)) parts.push(`<abbr title="${name}">${CAMPAIGN_ABBREV[bit]}</abbr>`);
        }
        return parts.length ? parts.join(', ') : '-';
    }
    return p ? escapeHtml(formatList(p)) : '-';
}

function formatSeason(season, code) {
    return season || 'Unspecified';
}

function getTotalPages() {
    return Math.ceil(filteredItems.length / itemsPerPage) || 1;
}

// Pagination controls exist twice: above the results (suffix "-top") and below them
const PAGINATION_SUFFIXES = ['', '-top'];

function updatePaginationUI() {
    const totalPages = getTotalPages();
    PAGINATION_SUFFIXES.forEach(suffix => {
        const cp = document.getElementById(`current-page${suffix}`);
        const tp = document.getElementById(`total-pages${suffix}`);
        if (cp) cp.textContent = currentPage;
        if (tp) tp.textContent = totalPages;
        ['first-page', 'prev-page'].forEach(id => {
            const btn = document.getElementById(id + suffix);
            if (btn) btn.disabled = currentPage === 1;
        });
        ['next-page', 'last-page'].forEach(id => {
            const btn = document.getElementById(id + suffix);
            if (btn) btn.disabled = currentPage === totalPages;
        });
    });
}

function goToPage(page, { scroll = true } = {}) {
    const target = Math.min(Math.max(page, 1), getTotalPages());
    if (target === currentPage) return;
    currentPage = target;
    displayResults();
    if (scroll) window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showGoToPagePrompt() {
    const totalPages = getTotalPages();
    const input = prompt(`Enter page number (1-${totalPages}):`, currentPage);
    if (input === null) return;

    const pageNum = parseInt(input);
    if (!isNaN(pageNum) && pageNum >= 1 && pageNum <= totalPages) {
        goToPage(pageNum);
    } else {
        alert('Please enter a valid page number.');
    }
}

function clearFilters() {
    filters.campaign = '';
    filters.season = '';
    filters.tier = '';
    filters.hours = '';
    filters.source = '';
    filters.ccOnly = false;
    filters.hideAiContent = false;
    filters.privateOnly = false;
    filters.search = '';

    ['campaign', 'season', 'tier', 'hours', 'source', 'search'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
    const ccOnly = document.getElementById('cc-only');
    if (ccOnly) ccOnly.checked = false;
    const hideAi = document.getElementById('hide-ai-content');
    if (hideAi) hideAi.checked = false;
    const privateOnly = document.getElementById('private-only');
    if (privateOnly) privateOnly.checked = false;

    applyFilters();
    updateURLFromFilters();
}

// Filter key -> form control id, for filters that can be removed individually
const FILTER_CONTROLS = {
    campaign: 'campaign',
    season: 'season',
    tier: 'tier',
    hours: 'hours',
    source: 'source',
    search: 'search',
    ccOnly: 'cc-only',
    hideAiContent: 'hide-ai-content',
    privateOnly: 'private-only',
};

function activeFilterLabel(key) {
    const val = filters[key];
    switch (key) {
        case 'campaign': return val;
        case 'season': return `Season: ${val}`;
        case 'tier': return `Tier ${val}`;
        case 'hours': return `${val} hr`;
        case 'source': {
            const opt = document.querySelector(`#source option[value="${CSS.escape(val)}"]`);
            return `Source: ${opt ? opt.textContent : val}`;
        }
        case 'search': return `Search: “${val}”`;
        case 'ccOnly': return 'Community content';
        case 'hideAiContent': return 'Hiding AI assisted';
        case 'privateOnly': return 'In private inventory';
    }
    return String(val);
}

function removeFilter(key) {
    const el = document.getElementById(FILTER_CONTROLS[key]);
    if (typeof filters[key] === 'boolean') {
        filters[key] = false;
        if (el) el.checked = false;
    } else {
        filters[key] = '';
        if (el) el.value = '';
    }
    applyFilters();
    updateURLFromFilters();
}

// Removable chips above the results, one per active filter
function renderActiveFilters() {
    const container = document.getElementById('active-filters');
    if (!container) return;
    container.innerHTML = Object.keys(FILTER_CONTROLS)
        .filter(key => filters[key])
        .map(key => {
            const label = escapeHtml(activeFilterLabel(key));
            return `<button type="button" class="active-filter" data-key="${key}" aria-label="Remove filter: ${label}">${label}<span class="remove" aria-hidden="true">×</span></button>`;
        })
        .join('');
    container.querySelectorAll('.active-filter').forEach(chip => {
        chip.addEventListener('click', () => {
            removeFilter(chip.dataset.key);
            // The chips were re-rendered; keep keyboard focus nearby
            (container.querySelector('.active-filter') || document.getElementById('toggle-filters'))?.focus();
        });
    });
}

function countActiveFilters() {
    return Object.keys(FILTER_CONTROLS).filter(key => filters[key]).length;
}

// Button reads "Show Filters (2)" when the panel is closed and filters are
// active, so a shared link with filters applied doesn't look unfiltered.
function updateFilterToggleLabel() {
    const toggleBtn = document.getElementById('toggle-filters');
    const panel = document.getElementById('filter-panel');
    if (!toggleBtn || !panel) return;
    const hidden = panel.classList.contains('hidden');
    const active = countActiveFilters();
    toggleBtn.textContent = hidden
        ? (active ? `Show Filters (${active})` : 'Show Filters')
        : 'Hide Filters';
    toggleBtn.setAttribute('aria-expanded', String(!hidden));
}

function toggleFilters() {
    const toggleBtn = document.getElementById('toggle-filters');
    const panel = document.getElementById('filter-panel');
    if (toggleBtn && panel) {
        panel.classList.toggle('hidden');
        updateFilterToggleLabel();
    }
}

function setupEventListeners() {
    ['campaign', 'tier', 'hours', 'season', 'source', 'sort', 'search'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener(el.tagName === 'INPUT' ? 'input' : 'change', e => {
            if (id === 'sort') {
                sortBy = e.target.value;
            } else {
                filters[id] = e.target.value;
            }
            applyFilters();
            updateURLFromFilters();
        });
    });

    // Bottom controls scroll back to the top; top controls are already in view
    PAGINATION_SUFFIXES.forEach(suffix => {
        const scroll = suffix === '';
        document.getElementById(`first-page${suffix}`)?.addEventListener('click', () => goToPage(1, { scroll }));
        document.getElementById(`prev-page${suffix}`)?.addEventListener('click', () => goToPage(currentPage - 1, { scroll }));
        document.getElementById(`next-page${suffix}`)?.addEventListener('click', () => goToPage(currentPage + 1, { scroll }));
        document.getElementById(`last-page${suffix}`)?.addEventListener('click', () => goToPage(getTotalPages(), { scroll }));
    });

    document.getElementById('cc-only')?.addEventListener('change', e => {
        filters.ccOnly = e.target.checked;
        applyFilters();
        updateURLFromFilters();
    });

    document.getElementById('hide-ai-content')?.addEventListener('change', e => {
        setHideAiContent(e.target.checked);
    });

    document.getElementById('private-only')?.addEventListener('change', e => {
        filters.privateOnly = e.target.checked;
        applyFilters();
        updateURLFromFilters();
    });

    document.getElementById('show-product-id')?.addEventListener('change', e => {
        filters.showProductId = e.target.checked;
        applyFilters();
        updateURLFromFilters();
    });

    document.getElementById('show-author')?.addEventListener('change', e => {
        filters.showAuthor = e.target.checked;
        applyFilters();
        updateURLFromFilters();
    });

    document.getElementById('view-card')?.addEventListener('change', () => setViewMode('card'));
    document.getElementById('view-grid')?.addEventListener('change', () => setViewMode('grid'));



    const toggleBtn = document.getElementById('toggle-filters');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleFilters);
    }

    document.getElementById('clear-filters')?.addEventListener('click', clearFilters);

    // Keyboard: Left/Right or A/D = prev/next page, Shift+Left/Right or W/S = first/last page,
    // G = go to page, F = toggle filters
    document.addEventListener('keydown', (e) => {
        // Leave browser shortcuts (Ctrl+F etc.) and form controls alone
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        const active = document.activeElement;
        if (active && (['INPUT', 'TEXTAREA', 'SELECT'].includes(active.tagName) || active.isContentEditable)) return;

        const key = e.key.toLowerCase();
        if (e.key === 'ArrowLeft') {
            goToPage(e.shiftKey ? 1 : currentPage - 1);
        } else if (e.key === 'ArrowRight') {
            goToPage(e.shiftKey ? getTotalPages() : currentPage + 1);
        } else if (key === 'a') {
            goToPage(currentPage - 1);
        } else if (key === 'd') {
            goToPage(currentPage + 1);
        } else if (key === 'w') {
            goToPage(1);
        } else if (key === 's') {
            goToPage(getTotalPages());
        } else if (key === 'g') {
            showGoToPagePrompt();
        } else if (key === 'f') {
            toggleFilters();
        }
    });

    // Go to page click listeners
    document.getElementById('goto-page-info-top')?.addEventListener('click', showGoToPagePrompt);
    document.getElementById('page-info')?.addEventListener('click', showGoToPagePrompt);

    // Listen for storage changes from other tabs (like the inventory manager)
    window.addEventListener('storage', (e) => {
        if (e.key === 'private_inventory') {
            console.log('Private inventory updated in another tab/window. Refreshing links...');
            if (e.newValue) {
                try {
                    filters.privateLinks = JSON.parse(e.newValue);
                } catch (err) {
                    console.error('Failed to parse updated private inventory:', err);
                    filters.privateLinks = {};
                }
            } else {
                filters.privateLinks = {};
            }
            applyFilters();
            displayResults();
        }
    });
}

function setViewMode(mode) {
    viewMode = mode;
    updateViewToggleButtons();
    displayResults();
    updateURLFromFilters();
}

function updateViewToggleButtons() {
    const vc = document.getElementById('view-card');
    const vg = document.getElementById('view-grid');
    if (!vc || !vg) return;

    vc.checked = viewMode === 'card';
    vg.checked = viewMode === 'grid';
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}