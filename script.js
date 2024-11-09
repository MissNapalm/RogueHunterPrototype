const map = L.map('map').setView([41.8781, -87.6298], 11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let layers = {};
let heatmaps = {};
let currentYear = 'all';
let isHeatmapMode = false;

async function fetchCrimeData() {
    const response = await fetch('/api/getCrimeData');
    return response.json();
}

function formatPopup(crime, crimeType) {
    return `
        <div class="popup-content">
            <div class="popup-title">${crimeType}</div>
            <div class="popup-detail"><strong>Date:</strong> ${crime.date}</div>
            <div class="popup-detail"><strong>Location:</strong> ${crime.block}</div>
            <div class="popup-detail"><strong>Details:</strong> ${crime.description || 'Not provided'}</div>
            <div class="popup-detail"><strong>Arrest Made:</strong> ${crime.arrest}</div>
        </div>
    `;
}

async function updateVisualization() {
    const crimeData = await fetchCrimeData();
    Object.keys(crimeData).forEach(crimeType => {
        // Update visualization logic for each crime type
    });
}

// Event listeners and additional functionality (similar to your initial script)
// updateVisualization();
