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
    ccOnly: false,
    privateOnly: false,
    showProductId: false,
    search: '',
    inventoryURL: '',
    privateLinks: {}
};

let sortBy = 'date-desc';
let viewMode = 'grid';

const CAMPAIGN_MAP = {
    1: 'Forgotten Realms',
    2: 'Eberron',
    4: 'Ravenloft',
    8: 'Dragonlance'
};

// Config
const baseURL = 'assets/data/';

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
                    luDate.textContent = formattedDate;
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
    document.getElementById('results').innerHTML = `<div class="p-4 text-red-600">Error loading catalog: ${err.message}</div>`;
}
}

async function loadPrivateInventory() {
    const params = new URLSearchParams(window.location.search);
    let invURL = params.get('inventory');
    
    // Check cookie if URL param is missing
    if (!invURL) {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('inventory_url='))
            ?.split('=')[1];
        if (cookieValue) invURL = decodeURIComponent(cookieValue);
    }

    if (invURL) {
        filters.inventoryURL = invURL;
        try {
            console.log('Fetching private inventory from:', invURL);
            const resp = await fetch(invURL);
            if (resp.ok) {
                filters.privateLinks = await resp.json();
                console.log(`Loaded ${Object.keys(filters.privateLinks).length} private links.`);
            }
        } catch (e) {
            console.warn('Failed to load private inventory:', e);
        }
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
    if (params.has('search')) filters.search = params.get('search');
    if (params.has('ccOnly')) filters.ccOnly = params.get('ccOnly') === 'true';
    if (params.has('privateOnly')) filters.privateOnly = params.get('privateOnly') === 'true';
    if (params.has('showProductId')) filters.showProductId = params.get('showProductId') === 'true';
    if (params.has('sort')) sortBy = params.get('sort');

    // Sync to DOM so dropdowns and search input show the URL state
    const campaignEl = document.getElementById('campaign');
    if (campaignEl) campaignEl.value = filters.campaign || '';
    const seasonEl = document.getElementById('season');
    if (seasonEl) seasonEl.value = filters.season || '';
    const tierEl = document.getElementById('tier');
    if (tierEl) tierEl.value = filters.tier || '';
    const hoursEl = document.getElementById('hours');
    if (hoursEl) hoursEl.value = filters.hours || '';
    const sortEl = document.getElementById('sort');
    if (sortEl) sortEl.value = sortBy || 'date-desc';
    const searchEl = document.getElementById('search');
    if (searchEl) searchEl.value = filters.search || '';
    const inventoryEl = document.getElementById('inventory-url');
    if (inventoryEl) inventoryEl.value = filters.inventoryURL || '';
    const ccOnlyEl = document.getElementById('cc-only');
    if (ccOnlyEl) ccOnlyEl.checked = filters.ccOnly || false;
    const privateOnlyEl = document.getElementById('private-only');
    if (privateOnlyEl) privateOnlyEl.checked = filters.privateOnly || false;
    const showProductIdEl = document.getElementById('show-product-id');
    if (showProductIdEl) showProductIdEl.checked = filters.showProductId || false;

    applyFilters();
}

function updateURLFromFilters() {
    const params = new URLSearchParams();
    if (filters.campaign) params.set('campaign', filters.campaign);
    if (filters.season) params.set('season', filters.season);
    if (filters.tier) params.set('tier', filters.tier);
    if (filters.hours) params.set('hours', filters.hours);
    if (filters.search) params.set('search', filters.search);
    if (filters.ccOnly) params.set('ccOnly', 'true');
    if (filters.privateOnly) params.set('privateOnly', 'true');
    if (filters.showProductId) params.set('showProductId', 'true');
    if (sortBy && sortBy !== 'date-desc') params.set('sort', sortBy);

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
        results = results.filter(adv => {
            const productId = String(adv.i).replace(/-\d+$/, '');
            return filters.privateLinks[adv.i] || filters.privateLinks[productId];
        });
    }

    if (filters.ccOnly) {
        results = results.filter(adv => adv.f && (adv.f & 1));
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

    updatePaginationUI();

    // Render
    const pageItems = filteredItems.slice(start, end);
    resultsDiv.innerHTML = '';

    if (viewMode === 'grid') {
        resultsDiv.className = 'overflow-x-auto';
        renderGridView(pageItems, resultsDiv);
    } else {
        resultsDiv.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';
        pageItems.forEach(adv => {
            resultsDiv.appendChild(createCard(adv));
        });
    }
}

// ... Rendering functions (Card/Grid) ...

function createCard(adventure) {
    const card = document.createElement('div');
    card.className = 'border rounded-xl p-4 shadow-lg hover:shadow-xl transition-shadow bg-white';

    const campaign = formatCampaigns(adventure.p) || 'Unspecified';
    const hours = formatHours(adventure.h);
    const season = formatSeason(adventure.s, adventure.c);
    const authors = formatList(adventure.a) || 'N/A';
    const dateAdded = adventure.d ? `${adventure.d.substring(0, 4)}-${adventure.d.substring(4, 6)}-${adventure.d.substring(6, 8)}` : 'N/A';

    const productId = String(adventure.i).replace(/-\d+$/, '');
    const url = adventure.u || `https://www.dmsguild.com/product/${productId}/?affiliate_id=171040`;
    const privateLink = filters.privateLinks[adventure.i] || filters.privateLinks[productId];

    card.innerHTML = `
        <div class="flex justify-between items-start">
            <a href="${url}" target="_blank" class="text-lg font-semibold mb-2 text-blue-600 hover:text-blue-800 block">
                ${adventure.n || 'Untitled'}
            </a>
            ${privateLink ? `
                <a href="${privateLink}" target="_blank" title="View Private PDF" class="ml-2 p-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                    </svg>
                </a>
            ` : ''}
        </div>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Code:</span> ${adventure.c || 'N/A'}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Author(s):</span> ${authors}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Campaign:</span> ${campaign}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Season:</span> ${season}</p>
        <p class="text-sm text-gray-600 mb-1">
            <span class="font-medium">Hours:</span> ${hours} &bull; 
            <span class="font-medium">Tier:</span> ${adventure.t !== null ? adventure.t : 'Unspecified'}
        </p>
        <p class="text-sm text-gray-500 mt-2 italic">Added: ${dateAdded}</p>
    `;
    return card;
}

function renderGridView(adventures, container) {
    const table = document.createElement('table');
    table.className = 'w-full border-collapse bg-white';

    const showProductId = filters.showProductId;

    table.innerHTML = `
        <thead class="bg-gray-100">
            <tr>
                ${showProductId ? '<th class="px-4 py-2 text-left border">ID</th>' : ''}
                <th class="px-4 py-2 text-left border">Code</th>
                <th class="px-4 py-2 text-left border">Title</th>
                <th class="px-4 py-2 text-left border">Tier</th>
                <th class="px-4 py-2 text-left border">Hours</th>
                <th class="px-4 py-2 text-left border">Campaign</th>
                <th class="px-4 py-2 text-left border">Added</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');
    adventures.forEach(adv => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        const dateAdded = adv.d ? `${adv.d.substring(0, 4)}-${adv.d.substring(4, 6)}-${adv.d.substring(6, 8)}` : 'N/A';
        const productId = String(adv.i).replace(/-\d+$/, '');
        const url = adv.u || `https://www.dmsguild.com/product/${productId}/?affiliate_id=171040`;
        const privateLink = filters.privateLinks[adv.i] || filters.privateLinks[productId];
        
        row.innerHTML = `
             ${showProductId ? `<td class="px-4 py-2 border text-sm">${productId}</td>` : ''}
             <td class="px-4 py-2 border">${adv.c || ''}</td>
             <td class="px-4 py-2 border">
                <div class="flex items-center justify-between">
                    <a href="${url}" target="_blank" class="text-blue-600 hover:underline">${adv.n}</a>
                    ${privateLink ? `
                        <a href="${privateLink}" target="_blank" class="ml-2 text-green-600 hover:text-green-800" title="Private PDF">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                            </svg>
                        </a>
                    ` : ''}
                </div>
             </td>
             <td class="px-4 py-2 border">${adv.t !== null ? adv.t : ''}</td>
             <td class="px-4 py-2 border">${formatHours(adv.h)}</td>
             <td class="px-4 py-2 border">${formatCampaigns(adv.p)}</td>
             <td class="px-4 py-2 border text-sm text-gray-500 italic">${dateAdded}</td>
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
    if (!val) return 'Unspecified';
    if (Array.isArray(val)) return val.join(', ') + ' Hours';
    return val + ' Hours';
}

function formatSeason(season, code) {
    return season || 'Unspecified';
}

function updatePaginationUI() {
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage) || 1;
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('total-pages').textContent = totalPages;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages;
}

function setupEventListeners() {
    ['campaign', 'tier', 'hours', 'season', 'sort', 'search'].forEach(id => {
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

    document.getElementById('prev-page')?.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; displayResults(); }
    });

    document.getElementById('cc-only')?.addEventListener('change', e => {
        filters.ccOnly = e.target.checked;
        applyFilters();
        updateURLFromFilters();
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

    document.getElementById('next-page')?.addEventListener('click', () => {
        const max = Math.ceil(filteredItems.length / itemsPerPage);
        if (currentPage < max) { currentPage++; displayResults(); }
    });

    document.getElementById('view-card')?.addEventListener('click', () => { viewMode = 'card'; updateViewToggleButtons(); displayResults(); });
    document.getElementById('view-grid')?.addEventListener('click', () => { viewMode = 'grid'; updateViewToggleButtons(); displayResults(); });
    
    document.getElementById('load-example-inventory')?.addEventListener('click', () => {
        const exampleURL = window.location.origin + (baseURL.startsWith('/') ? '' : '/') + baseURL.replace('assets/data/', '') + 'example_private_intentory.json';
        const input = document.getElementById('inventory-url');
        if (input) {
            input.value = exampleURL;
            
            // Helpful hint for the user
            alert("Example inventory loaded! Select '1 - Tyranny of Dragons' in the Season filter to see the green private PDF links.");
            
            // Auto-select Season 1 to show the markers
            const seasonEl = document.getElementById('season');
            if (seasonEl) {
                // We need to find the option that starts with "1"
                for (let i = 0; i < seasonEl.options.length; i++) {
                    if (seasonEl.options[i].value.startsWith("1 -")) {
                        seasonEl.value = seasonEl.options[i].value;
                        filters.season = seasonEl.value;
                        break;
                    }
                }
            }
            
            // Optionally trigger the apply logic immediately
            document.getElementById('save-inventory')?.click();
        }
    });

    document.getElementById('save-inventory')?.addEventListener('click', () => {
        const url = document.getElementById('inventory-url')?.value.trim();
        if (url) {
            // Set cookie for 1 year
            const expires = new Date();
            expires.setFullYear(expires.getFullYear() + 1);
            document.cookie = `inventory_url=${encodeURIComponent(url)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
            
            // Reload page to apply
            const params = new URLSearchParams(window.location.search);
            params.set('inventory', url);
            window.location.search = params.toString();
        } else {
            // Clear cookie
            document.cookie = `inventory_url=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
            const params = new URLSearchParams(window.location.search);
            params.delete('inventory');
            window.location.search = params.toString();
        }
    });

    const toggleBtn = document.getElementById('toggle-filters');
    const panel = document.getElementById('filter-panel');
    if (toggleBtn && panel) {
        toggleBtn.addEventListener('click', () => {
            panel.classList.toggle('hidden');
            toggleBtn.textContent = panel.classList.contains('hidden') ? 'Show Filters' : 'Hide Filters';
        });
    }
}

function updateViewToggleButtons() {
    const vc = document.getElementById('view-card');
    const vg = document.getElementById('view-grid');
    if (!vc || !vg) return;

    if (viewMode === 'card') {
        vc.classList.add('bg-blue-500', 'text-white'); vc.classList.remove('hover:bg-gray-100');
        vg.classList.remove('bg-blue-500', 'text-white'); vg.classList.add('hover:bg-gray-100');
    } else {
        vg.classList.add('bg-blue-500', 'text-white'); vg.classList.remove('hover:bg-gray-100');
        vc.classList.remove('bg-blue-500', 'text-white'); vc.classList.add('hover:bg-gray-100');
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}