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
    hours: ''
};

let baseURL = '';
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    baseURL = '/assets/data/';
} else {
    baseURL = '/al_adventure_catalog/assets/data/';
}

// Fetch and load the JSON data
fetch(baseURL + 'all_adventures.json')
    .then(response => response.json())
    .then(data => {
        adventures = data;
        populateFilters(adventures);
        updateItemsPerPage(); // Set initial items per page
        applyFilters();
        setupEventListeners();
    });

window.addEventListener('resize', updateItemsPerPage); // Update on resize

function populateFilters(adventures) {
    const campaigns = [...new Set(adventures.map(a => a.campaigns).flat())].sort();
    const tiers = [...new Set(adventures.map(a => a.tiers).filter(t => t !== null).sort((a, b) => a - b))];
    const hours = [...new Set(adventures.map(a => a.hours).flat().filter(h => h !== null).sort((a, b) => a - b))];

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

function setupEventListeners() {
    // Add event listeners for filters
    ['campaign', 'tier', 'hours'].forEach(filter => {
        document.getElementById(filter).addEventListener('change', (e) => {
            filters[filter] = e.target.value;
            currentPage = 1; // Reset to first page when filtering
            applyFilters();
        });
    });

    // Add pagination event listeners
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            displayResults();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        if (currentPage < getTotalPages()) {
            currentPage++;
            displayResults();
        }
    });
}

function applyFilters() {
    filteredAdventures = adventures.filter(adventure => {
        const campaignMatch = !filters.campaign || (
            Array.isArray(adventure.campaigns)
                ? adventure.campaigns.includes(filters.campaign)
                : false // Should not happen if data is consistent
        );

        const hoursMatch = !filters.hours || (
            Array.isArray(adventure.hours)
                ? adventure.hours.includes(parseInt(filters.hours))
                : false // Should not happen if data is consistent
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
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, filteredAdventures.length);
    const currentPageData = filteredAdventures.slice(startIndex, endIndex);
    console.log('Current page data count:', currentPageData.length);

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    currentPageData.forEach(adventure => {
        const card = document.createElement('div');
        card.className = 'border rounded-xl p-4 shadow-lg hover:shadow-xl transition-shadow';

        // Handle campaign display for both array and single value cases
        const campaignDisplay = Array.isArray(adventure.campaigns)
            ? adventure.campaigns.join(', ')
            : adventure.campaigns; // Should be campaigns now

        const hoursDisplay = Array.isArray(adventure.hours)
            ? adventure.hours.join('-') + ' Hours'
            : adventure.hours + ' Hours';

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