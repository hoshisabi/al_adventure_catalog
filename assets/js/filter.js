let adventures = [];
let filteredAdventures = [];
let currentPage = 1;
let itemsPerPage;

function updateItemsPerPage() {
    if (window.innerWidth >= 992) { // Example breakpoint for larger screens
        itemsPerPage = 48;
    } else {
        itemsPerPage = 24;
    }
    currentPage = 1; // Reset to first page when itemsPerPage changes
    displayResults(); // Re-render with new item count
}

let filters = {
    campaign: '',
    season: '',
    tier: '',
    hours: '',
    dcOnly: false,
    search: ''
};

let sortBy = 'date-desc'; // Default sort: newest first
let viewMode = 'card'; // 'card' or 'grid'

// Map season names to their numeric values for display
const SEASON_NUMBERS = {
    'Tyranny of Dragons': 1,
    'Elemental Evil': 2,
    'Rage of Demons': 3,
    'Curse of Strahd': 4,
    "Storm King's Thunder": 5,
    "Tales From the Yawning Portal": 6,
    "Tomb of Annihilation": 7,
    'Waterdeep': 8,
    'Avernus Rising': 9,
    'Plague of Ancients': 10
};

// Named seasons that don't have numeric values (Eberron, Ravenloft, etc.)
const NAMED_SEASONS = [
    'The Wild Beyond the Witchlight',
    'Spelljammer',
    'Planescape',
    'Oracle of War',
    'Embers of War',
    'Salvage Missions',
    'Eberron Dungeoncraft',
    'Ravenloft Mist Hunters',
    'Ravenloft Dungeoncraft'
];

function formatSeason(season, code) {
    if (!season || season === 'Unknown' || season === 'Unspecified') {
        return 'Unspecified';
    }
    
    // Check if it's a numeric season (1-10)
    const seasonNum = SEASON_NUMBERS[season];
    if (seasonNum) {
        return `Season ${seasonNum} ${season}`;
    }
    
    // For named programs/seasons (WBW-DC, SJ-DC, Eberron, Ravenloft, etc.), just return the name
    // These don't have numeric season numbers
    return season;
}

function formatValue(value, defaultValue = 'Unspecified') {
    if (value === null || value === undefined || value === '' || value === 0 || value === '0') {
        return defaultValue;
    }
    return value;
}

// DC code prefixes (from DC_CAMPAIGNS)
const DC_CODE_PREFIXES = [
    'FR-DC', 'DL-DC', 'EB-DC', 'PS-DC', 'RV-DC', 'SJ-DC', 'WBW-DC',
    'DC-POA', 'PO-BK', 'BMG-DRW', 'BMG-MOON', 'BMG-DL', 'EB-SM', 'CCC-'
];

function isDCCode(code) {
    if (!code) return false;
    const codeUpper = code.toUpperCase();
    return DC_CODE_PREFIXES.some(prefix => codeUpper.startsWith(prefix));
}

// Determine baseURL based on current path
// If running locally with --baseurl "", path will be "/"
// If running with baseurl, path will include the baseurl
let baseURL = '';
const pathname = window.location.pathname;
if (pathname.startsWith('/al_adventure_catalog/')) {
    baseURL = '/al_adventure_catalog/assets/data/';
} else {
    // Local development or serving with --baseurl ""
    baseURL = '/assets/data/';
}

// Wait for DOM to be ready, then fetch and load the JSON data
function startLoading() {
    console.log('Starting to load adventures...');
    console.log('Base URL:', baseURL);
    console.log('Full URL:', baseURL + 'all_adventures.json');
    
    fetch(baseURL + 'all_adventures.json')
        .then(response => {
            console.log('Fetch response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                console.error('Expected array but got:', typeof data, data);
                return;
            }
            adventures = data;
            console.log(`Loaded ${adventures.length} adventures`);
            console.log('Sample adventure:', adventures[0]);
            
            initializeFilters();
        })
        .catch(error => {
            console.error('Error loading adventures:', error);
            console.error('Attempted URL:', baseURL + 'all_adventures.json');
            const resultsDiv = document.getElementById('results');
            if (resultsDiv) {
                resultsDiv.innerHTML = `<div class="text-red-600 p-4">Error loading adventures: ${error.message}. Check console for details.</div>`;
            }
        });
}

// Start loading when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startLoading);
} else {
    // DOM is already ready
    startLoading();
}

window.addEventListener('resize', updateItemsPerPage); // Update on resize

function parseHoursString(hoursStr) {
    if (!hoursStr) {
        return [];
    }
    const hoursList = [];
    hoursStr.split(',').forEach(part => {
        if (part.includes('-')) {
            const [start, end] = part.split('-').map(Number);
            for (let i = start; i <= end; i++) {
                hoursList.push(i);
            }
        } else {
            hoursList.push(Number(part));
        }
    });
    return hoursList;
}

// Season name normalization: map synonyms to canonical names
const SEASON_NORMALIZATION = {
    "Icewind Dale": "Plague of Ancients",
};

function normalizeSeason(season) {
    if (!season) return season;
    return SEASON_NORMALIZATION[season] || season;
}

function populateFilters(adventures) {
    // Filter out null, empty, and 'null' string values for campaigns
    const campaigns = [...new Set(adventures.map(a => {
        const camp = Array.isArray(a.campaigns) ? a.campaigns : [a.campaigns];
        return camp.filter(c => c && c !== '' && c !== 'null');
    }).flat())].sort();
    
    // Normalize season names to handle synonyms (e.g., "Icewind Dale" -> "Plague of Ancients")
    // Filter out null/undefined/empty values
    const seasons = [...new Set(adventures.map(a => normalizeSeason(a.season)).filter(s => s !== null && s !== undefined && s !== ''))].sort();
    
    // Convert tiers to numbers and ensure proper deduplication
    // Filter out null/undefined/0, convert to numbers, then deduplicate with Set, then sort
    const tiers = [...new Set(adventures.map(a => a.tiers).filter(t => t !== null && t !== undefined && t !== 0 && t !== '0').map(t => Number(t)))].sort((a, b) => a - b);
    
    // Filter out 0 values for hours
    const hours = [...new Set(adventures.map(a => parseHoursString(a.hours)).flat().filter(h => h !== null && h !== 0 && h !== '0').sort((a, b) => a - b))];

    populateDropdown('campaign', campaigns, 'All Campaigns');
    populateDropdown('season', seasons, 'All Seasons');
    populateDropdown('tier', tiers, 'All Tiers');
    populateDropdown('hours', hours, 'All Lengths');
}

function populateDropdown(id, values, defaultOptionText) {
    const selectElement = document.getElementById(id);
    selectElement.innerHTML = ''; // Clear existing options

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = defaultOptionText;
    selectElement.appendChild(defaultOption);

    values.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        selectElement.appendChild(option);
    });
}

function initializeFilters() {
    populateFilters(adventures);
    updateItemsPerPage(); // Set initial items per page
    setupEventListeners();
    updateViewToggleButtons(); // Set initial view toggle state
    applyFilters(); // Apply filters after everything is set up
}

function setupEventListeners() {
    // Add event listeners for filters
    ['campaign', 'season', 'tier', 'hours'].forEach(filter => {
        const element = document.getElementById(filter);
        if (element) {
            element.addEventListener('change', (e) => {
                filters[filter] = e.target.value;
                // applyFilters() will reset currentPage and sort all filtered data
                applyFilters();
            });
        }
    });
    
    // Add event listener for sort dropdown
    const sortElement = document.getElementById('sort');
    if (sortElement) {
        sortElement.addEventListener('change', (e) => {
            sortBy = e.target.value;
            // applyFilters() will reset currentPage and sort all filtered data
            applyFilters();
        });
    }

    // Add event listener for DC-only checkbox
    const dcOnlyCheckbox = document.getElementById('dc-only');
    if (dcOnlyCheckbox) {
        dcOnlyCheckbox.addEventListener('change', (e) => {
            filters.dcOnly = e.target.checked;
            // applyFilters() will reset currentPage and sort all filtered data
            applyFilters();
        });
    }

    // Add event listener for search input with debouncing
    const searchInput = document.getElementById('search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filters.search = e.target.value.trim();
                currentPage = 1; // Reset to first page when searching
                applyFilters();
            }, 300); // 300ms debounce
        });
    }

    // Add pagination event listeners
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                displayResults();
            }
        });
    }
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (currentPage < getTotalPages()) {
                currentPage++;
                displayResults();
            }
        });
    }

    // Add view toggle event listeners
    const viewCardButton = document.getElementById('view-card');
    const viewGridButton = document.getElementById('view-grid');
    if (viewCardButton) {
        viewCardButton.addEventListener('click', () => {
            viewMode = 'card';
            updateViewToggleButtons();
            displayResults();
        });
    }
    if (viewGridButton) {
        viewGridButton.addEventListener('click', () => {
            viewMode = 'grid';
            updateViewToggleButtons();
            displayResults();
        });
    }

    // Add filter toggle event listener
    const toggleFiltersButton = document.getElementById('toggle-filters');
    const filterPanel = document.getElementById('filter-panel');
    if (toggleFiltersButton && filterPanel) {
        toggleFiltersButton.addEventListener('click', () => {
            const isHidden = filterPanel.classList.contains('hidden');
            if (isHidden) {
                filterPanel.classList.remove('hidden');
                toggleFiltersButton.textContent = 'Hide Filters';
            } else {
                filterPanel.classList.add('hidden');
                toggleFiltersButton.textContent = 'Show Filters';
            }
        });
    }
}

function updateViewToggleButtons() {
    const viewCardButton = document.getElementById('view-card');
    const viewGridButton = document.getElementById('view-grid');
    if (viewCardButton && viewGridButton) {
        if (viewMode === 'card') {
            viewCardButton.classList.add('active', 'bg-blue-500', 'text-white');
            viewCardButton.classList.remove('hover:bg-gray-100');
            viewGridButton.classList.remove('active', 'bg-blue-500', 'text-white');
            viewGridButton.classList.add('hover:bg-gray-100');
        } else {
            viewGridButton.classList.add('active', 'bg-blue-500', 'text-white');
            viewGridButton.classList.remove('hover:bg-gray-100');
            viewCardButton.classList.remove('active', 'bg-blue-500', 'text-white');
            viewCardButton.classList.add('hover:bg-gray-100');
        }
    }
}

function applyFilters() {
    // Filter all adventures based on current filter criteria
    filteredAdventures = adventures.filter(adventure => {
        // DC-only filter: if enabled, only show adventures with DC codes
        if (filters.dcOnly && !isDCCode(adventure.code)) {
            return false;
        }

        // Search filter: search in title, code, and authors (case-insensitive)
        if (filters.search) {
            const searchLower = filters.search.toLowerCase();
            const titleMatch = adventure.title && adventure.title.toLowerCase().includes(searchLower);
            const codeMatch = adventure.code && adventure.code.toLowerCase().includes(searchLower);
            const authorsMatch = adventure.authors && Array.isArray(adventure.authors) && 
                adventure.authors.some(author => author && author.toLowerCase().includes(searchLower));
            if (!titleMatch && !codeMatch && !authorsMatch) {
                return false;
            }
        }

        const campaignMatch = !filters.campaign || (
            Array.isArray(adventure.campaigns)
                ? adventure.campaigns.includes(filters.campaign)
                : false // Should not happen if data is consistent
        );

        const hoursMatch = !filters.hours || (
            parseHoursString(adventure.hours).includes(parseInt(filters.hours))
        );

        // Normalize season for comparison to handle synonyms
        const normalizedAdventureSeason = normalizeSeason(adventure.season);
        const seasonMatch = !filters.season || normalizedAdventureSeason === filters.season;

        return campaignMatch &&
            seasonMatch &&
            (!filters.tier || adventure.tiers === parseInt(filters.tier)) &&
            hoursMatch;
    });

    // Sort ALL filtered adventures (not just current page) before pagination
    sortAdventures();

    // Reset to first page when filters/sort change
    currentPage = 1;

    displayResults();
}

function sortAdventures() {
    const [sortField, sortDirection] = sortBy.split('-');
    
    filteredAdventures.sort((a, b) => {
        let aValue, bValue;
        
        switch (sortField) {
            case 'title':
                aValue = (a.title || '').toLowerCase();
                bValue = (b.title || '').toLowerCase();
                break;
            case 'code':
                aValue = (a.code || '').toLowerCase();
                bValue = (b.code || '').toLowerCase();
                break;
            case 'date':
                // Parse date_created if it's a string, otherwise use as-is
                aValue = a.date_created ? (typeof a.date_created === 'string' ? new Date(a.date_created) : a.date_created) : new Date(0);
                bValue = b.date_created ? (typeof b.date_created === 'string' ? new Date(b.date_created) : b.date_created) : new Date(0);
                break;
            default:
                return 0;
        }
        
        let comparison = 0;
        if (sortField === 'date') {
            comparison = aValue - bValue; // For dates, subtract directly
        } else {
            if (aValue < bValue) comparison = -1;
            else if (aValue > bValue) comparison = 1;
        }
        
        return sortDirection === 'desc' ? -comparison : comparison;
    });
}

function getTotalPages() {
    return Math.ceil(filteredAdventures.length / itemsPerPage);
}

function displayResults() {
    console.log('Displaying results. Filtered adventures:', filteredAdventures.length);
    console.log('Items per page:', itemsPerPage);
    console.log('Current page:', currentPage);
    
    if (!itemsPerPage) {
        console.error('itemsPerPage is not set!');
        updateItemsPerPage();
        return;
    }
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, filteredAdventures.length);
    const currentPageData = filteredAdventures.slice(startIndex, endIndex);
    console.log('Current page data count:', currentPageData.length);

    const resultsDiv = document.getElementById('results');
    if (!resultsDiv) {
        console.error('Results div not found!');
        return;
    }
    resultsDiv.innerHTML = '';

    // Update results container class based on view mode
    if (viewMode === 'grid') {
        resultsDiv.className = 'overflow-x-auto';
        // Create table structure for grid view
        const table = document.createElement('table');
        table.className = 'w-full border-collapse';
        table.setAttribute('role', 'table');
        
        // Create table header
        const thead = document.createElement('thead');
        thead.className = 'bg-gray-100 sticky top-0 z-10';
        const headerRow = document.createElement('tr');
        headerRow.className = 'border-b-2 border-gray-300';
        headerRow.innerHTML = `
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Title</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Code</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Author(s)</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Campaign</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Season</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700 border-r border-gray-300">Hours</th>
            <th class="px-4 py-2 text-left font-semibold text-sm text-gray-700">Tier</th>
        `;
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create table body
        const tbody = document.createElement('tbody');
        tbody.id = 'grid-tbody';
        table.appendChild(tbody);
        
        resultsDiv.innerHTML = '';
        resultsDiv.appendChild(table);
    } else {
        resultsDiv.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';
    }

    if (viewMode === 'grid') {
        const tbody = document.getElementById('grid-tbody');
        if (tbody) {
            tbody.innerHTML = '';
            currentPageData.forEach(adventure => {
                tbody.appendChild(createGridRow(adventure));
            });
        }
    } else {
        currentPageData.forEach(adventure => {
            resultsDiv.appendChild(createCard(adventure));
        });
    }

    // Update pagination UI
    const totalPages = getTotalPages();
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('total-pages').textContent = totalPages;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage === totalPages;

    // Update results info
    document.getElementById('showing-start').textContent = startIndex + 1;
    document.getElementById('showing-end').textContent = endIndex;
    document.getElementById('total-results').textContent = filteredAdventures.length;

    // Scroll to top of page
    window.scrollTo(0, 0);
}

function createCard(adventure) {
    const card = document.createElement('div');
    card.className = 'border rounded-xl p-4 shadow-lg hover:shadow-xl transition-shadow';

    // Handle campaign display for both array and single value cases
    let campaignDisplay = Array.isArray(adventure.campaigns)
        ? adventure.campaigns.filter(c => c && c !== '' && c !== 'null').join(', ')
        : (adventure.campaigns && adventure.campaigns !== '' && adventure.campaigns !== 'null' ? adventure.campaigns : null);
    campaignDisplay = campaignDisplay || 'Unspecified';

    // Handle hours display
    let hoursDisplay = 'Unspecified';
    if (adventure.hours) {
        if (Array.isArray(adventure.hours)) {
            const hoursList = adventure.hours.filter(h => h && h !== '0' && h !== 0);
            hoursDisplay = hoursList.length > 0 ? hoursList.join(', ') + ' Hours' : 'Unspecified';
        } else if (adventure.hours !== '0' && adventure.hours !== 0) {
            hoursDisplay = adventure.hours + ' Hours';
        }
    }
    
    // Handle authors display
    const authorsDisplay = adventure.authors && Array.isArray(adventure.authors) && adventure.authors.length > 0
        ? adventure.authors.join(', ')
        : 'N/A';
    
    // Handle season display
    const seasonDisplay = formatSeason(adventure.season, adventure.code);
    
    // Handle tier display
    const tierDisplay = formatValue(adventure.tiers, 'Unspecified');

    card.innerHTML = `
        <a href="${adventure.url}" target="_blank" class="text-lg font-semibold mb-2 text-blue-600 hover:text-blue-800 block">${adventure.title || adventure.full_title || 'Untitled'}</a>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Code:</span> ${adventure.code || 'N/A'}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Author(s):</span> ${authorsDisplay}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Campaign:</span> ${campaignDisplay}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Season:</span> ${seasonDisplay}</p>
        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">Hours:</span> ${hoursDisplay} &bull; <span class="font-medium">Tier:</span> ${tierDisplay}</p>
    `;
    return card;
}

function createGridRow(adventure) {
    const row = document.createElement('tr');
    row.className = 'border-b border-gray-200 hover:bg-gray-50 transition-colors';

    // Handle campaign display for both array and single value cases
    let campaignDisplay = Array.isArray(adventure.campaigns)
        ? adventure.campaigns.filter(c => c && c !== '' && c !== 'null').join(', ')
        : (adventure.campaigns && adventure.campaigns !== '' && adventure.campaigns !== 'null' ? adventure.campaigns : null);
    campaignDisplay = campaignDisplay || 'Unspecified';

    // Handle hours display
    let hoursDisplay = 'Unspecified';
    if (adventure.hours) {
        if (Array.isArray(adventure.hours)) {
            const hoursList = adventure.hours.filter(h => h && h !== '0' && h !== 0);
            hoursDisplay = hoursList.length > 0 ? hoursList.join(', ') : 'Unspecified';
        } else if (adventure.hours !== '0' && adventure.hours !== 0) {
            hoursDisplay = adventure.hours;
        }
    }
    
    // Handle authors display
    const authorsDisplay = adventure.authors && Array.isArray(adventure.authors) && adventure.authors.length > 0
        ? adventure.authors.join(', ')
        : 'N/A';
    
    // Handle season display
    const seasonDisplay = formatSeason(adventure.season, adventure.code);
    
    // Handle tier display
    const tierDisplay = formatValue(adventure.tiers, 'Unspecified');

    row.innerHTML = `
        <td class="px-4 py-2 border-r border-gray-300">
            <a href="${adventure.url}" target="_blank" class="text-base font-semibold text-blue-600 hover:text-blue-800">${adventure.title || adventure.full_title || 'Untitled'}</a>
        </td>
        <td class="px-4 py-2 text-sm text-gray-600 border-r border-gray-300">${adventure.code || 'N/A'}</td>
        <td class="px-4 py-2 text-sm text-gray-600 border-r border-gray-300">${authorsDisplay}</td>
        <td class="px-4 py-2 text-sm text-gray-600 border-r border-gray-300">${campaignDisplay}</td>
        <td class="px-4 py-2 text-sm text-gray-600 border-r border-gray-300">${seasonDisplay}</td>
        <td class="px-4 py-2 text-sm text-gray-600 border-r border-gray-300">${hoursDisplay}</td>
        <td class="px-4 py-2 text-sm text-gray-600">${tierDisplay}</td>
    `;
    return row;
}