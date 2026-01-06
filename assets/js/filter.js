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
    dcOnly: false,
    search: ''
};

let sortBy = 'date-desc';
let viewMode = 'card';

// Config
let baseURL = '';
const pathname = window.location.pathname;
if (pathname.startsWith('/al_adventure_catalog/')) {
    baseURL = '/al_adventure_catalog/assets/data/';
} else {
    baseURL = '/assets/data/';
}

// Initialization
async function initialize() {
    console.log('Initializing Lean Catalog...');

    try {
        const resp = await fetch(baseURL + 'catalog.json');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        catalog = await resp.json();

        console.log(`Loaded ${catalog.length} adventures.`);

        // Populate Dropdowns from Data
        populateFilterUI();

        // Initial Display
        filteredItems = [...catalog]; // Default: no filter
        updateItemsPerPage();
        setupEventListeners();
        updateViewToggleButtons();

        applyFilters();

    } catch (err) {
        console.error('Failed to initialize:', err);
        document.getElementById('results').innerHTML = `<div class="p-4 text-red-600">Error loading catalog: ${err.message}</div>`;
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
    // 1. Campaigns (ca)
    // flatten all campaigns
    const allCampaigns = new Set();
    catalog.forEach(adv => {
        if (Array.isArray(adv.p)) {
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

    // 4. Seasons (s)
    // Use ONLY the explicit season field which should be normalized by backend
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
    if (filters.campaign) {
        results = results.filter(adv => {
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
        results = results.filter(adv => {
            // Explicit match
            if (adv.s && String(adv.s) === filters.season) return true;
            return false;
        });
    }

    if (filters.dcOnly) {
        // Logic for 'DC Only'. 
    }

    if (filters.search) {
        const q = filters.search.toLowerCase();
        results = results.filter(adv => {
            return (adv.n && adv.n.toLowerCase().includes(q)) ||
                (adv.c && adv.c.toLowerCase().includes(q)) ||
                (adv.a && typeof adv.a === 'string' && adv.a.toLowerCase().includes(q));
        });
    }

    // 2. Sort
    const [field, dir] = sortBy.split('-');

    results.sort((a, b) => {
        let valA, valB;

        if (field === 'date') {
            valA = a.d || '';
            valB = b.d || '';
        } else if (field === 'title') {
            valA = (a.n || '').toLowerCase();
            valB = (b.n || '').toLowerCase();
        } else if (field === 'code') {
            valA = (a.c || '').toLowerCase();
            valB = (b.c || '').toLowerCase();
        }

        if (valA < valB) return dir === 'asc' ? -1 : 1;
        if (valA > valB) return dir === 'asc' ? 1 : -1;
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

    const campaign = formatList(adventure.p) || 'Unspecified';
    const hours = formatHours(adventure.h);
    const season = formatSeason(adventure.s, adventure.c);
    const authors = formatList(adventure.a) || 'N/A';

    card.innerHTML = `
        <a href="${adventure.u || '#'}" target="_blank" class="text-lg font-semibold mb-2 text-blue-600 hover:text-blue-800 block">
            ${adventure.n || 'Untitled'}
        </a>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Code:</span> ${adventure.c || 'N/A'}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Author(s):</span> ${authors}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Campaign:</span> ${campaign}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Season:</span> ${season}</p>
        <p class="text-sm text-gray-600 mb-1">
            <span class="font-medium">Hours:</span> ${hours} &bull; 
            <span class="font-medium">Tier:</span> ${adventure.t !== null ? adventure.t : 'Unspecified'}
        </p>
    `;
    return card;
}

function renderGridView(adventures, container) {
    const table = document.createElement('table');
    table.className = 'w-full border-collapse bg-white';

    table.innerHTML = `
        <thead class="bg-gray-100">
            <tr>
                <th class="px-4 py-2 text-left border">Title</th>
                <th class="px-4 py-2 text-left border">Code</th>
                <th class="px-4 py-2 text-left border">Hours</th>
                <th class="px-4 py-2 text-left border">Campaign</th>
                <th class="px-4 py-2 text-left border">Tier</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');
    adventures.forEach(adv => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        row.innerHTML = `
             <td class="px-4 py-2 border"><a href="${adv.u}" target="_blank" class="text-blue-600 hover:underline">${adv.n}</a></td>
             <td class="px-4 py-2 border">${adv.c || ''}</td>
             <td class="px-4 py-2 border">${formatHours(adv.h)}</td>
             <td class="px-4 py-2 border">${formatList(adv.p)}</td>
             <td class="px-4 py-2 border">${adv.t !== null ? adv.t : ''}</td>
        `;
        tbody.appendChild(row);
    });

    container.appendChild(table);
}

function formatList(val) {
    if (Array.isArray(val)) return val.filter(x => x).join(', ');
    return val;
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
            filters[id] = e.target.value;
            applyFilters();
        });
    });

    document.getElementById('prev-page')?.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; displayResults(); }
    });
    document.getElementById('next-page')?.addEventListener('click', () => {
        const max = Math.ceil(filteredItems.length / itemsPerPage);
        if (currentPage < max) { currentPage++; displayResults(); }
    });

    document.getElementById('view-card')?.addEventListener('click', () => { viewMode = 'card'; updateViewToggleButtons(); displayResults(); });
    document.getElementById('view-grid')?.addEventListener('click', () => { viewMode = 'grid'; updateViewToggleButtons(); displayResults(); });

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