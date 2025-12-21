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
    tier: '',
    hours: '',
    dcOnly: false,
    search: ''
};

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

function populateFilters(adventures) {
    const campaigns = [...new Set(adventures.map(a => Array.isArray(a.campaigns) ? a.campaigns : [a.campaigns]).flat())].sort();
    const tiers = [...new Set(adventures.map(a => a.tiers).filter(t => t !== null).sort((a, b) => a - b))];
    const hours = [...new Set(adventures.map(a => parseHoursString(a.hours)).flat().filter(h => h !== null).sort((a, b) => a - b))];

    populateDropdown('campaign', campaigns, 'All Campaigns');
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
    applyFilters(); // Apply filters after everything is set up
}

function setupEventListeners() {
    // Add event listeners for filters
    ['campaign', 'tier', 'hours'].forEach(filter => {
        const element = document.getElementById(filter);
        if (element) {
            element.addEventListener('change', (e) => {
                filters[filter] = e.target.value;
                currentPage = 1; // Reset to first page when filtering
                applyFilters();
            });
        }
    });

    // Add event listener for DC-only checkbox
    const dcOnlyCheckbox = document.getElementById('dc-only');
    if (dcOnlyCheckbox) {
        dcOnlyCheckbox.addEventListener('change', (e) => {
            filters.dcOnly = e.target.checked;
            currentPage = 1; // Reset to first page when filtering
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
}

function applyFilters() {
    filteredAdventures = adventures.filter(adventure => {
        // DC-only filter: if enabled, only show adventures with DC codes
        if (filters.dcOnly && !isDCCode(adventure.code)) {
            return false;
        }

        // Search filter: search in title and code (case-insensitive)
        if (filters.search) {
            const searchLower = filters.search.toLowerCase();
            const titleMatch = adventure.title && adventure.title.toLowerCase().includes(searchLower);
            const codeMatch = adventure.code && adventure.code.toLowerCase().includes(searchLower);
            if (!titleMatch && !codeMatch) {
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

        return campaignMatch &&
            (!filters.tier || adventure.tiers === parseInt(filters.tier)) &&
            hoursMatch;
    });

    displayResults();
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

    currentPageData.forEach(adventure => {
        const card = document.createElement('div');
        card.className = 'border rounded-xl p-4 shadow-lg hover:shadow-xl transition-shadow';

        // Handle campaign display for both array and single value cases
        const campaignDisplay = Array.isArray(adventure.campaigns)
            ? adventure.campaigns.join(', ')
            : adventure.campaigns; // Should be campaigns now

        const hoursDisplay = adventure.hours ? adventure.hours + ' Hours' : 'N/A';

        card.innerHTML = `
            <a href="${adventure.url}" target="_blank" class="text-lg font-semibold mb-2 text-blue-600 hover:text-blue-800">${adventure.title}</a>
            <p class="text-sm text-gray-600 mb-1">Code: ${adventure.code}</p>
            <p class="text-sm text-gray-600 mb-1">Campaign: ${campaignDisplay}</p>
            <p class="text-sm text-gray-600 mb-1">Hours: ${hoursDisplay} &bull; Tier: ${adventure.tiers}</p>
        `;
        resultsDiv.appendChild(card);
    });

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