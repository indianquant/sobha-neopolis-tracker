// Sobha Neopolis Listings Web Explorer
const listingsData = [
  {
    id: 1,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 1 of 18)",
    price_raw: 24500000,
    price_formatted: "₹2.45 Cr",
    sqft: 1611,
    floor: 1,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa99ecc98f9c9a10198f9fa7dae223a/detail"
  },
  {
    id: 2,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis, Panathur (Floor 1)",
    price_raw: 24800000,
    price_formatted: "₹2.48 Cr",
    sqft: 1611,
    floor: 1,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9af849f707ed7019f70f048ab2d46/detail"
  },
  {
    id: 3,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 2 of 15)",
    price_raw: 24000000,
    price_formatted: "₹2.40 Cr",
    sqft: 1611,
    floor: 2,
    total_floor: 15,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9a2489c8fddb1019c902f67bc1b7b/detail"
  },
  {
    id: 4,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 3 of 18)",
    price_raw: 25000000,
    price_formatted: "₹2.50 Cr",
    sqft: 1611,
    floor: 3,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8a9fa18495a516120195a52793e5043a/detail"
  },
  {
    id: 5,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis, Balagere (Floor 3)",
    price_raw: 27000000,
    price_formatted: "₹2.70 Cr",
    sqft: 1611,
    floor: 3,
    total_floor: 19,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-balagere-bangalore/8a9fbd83953da68501953e0c9ad61875/detail"
  },
  {
    id: 6,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 3 of 18, 1613 sqft)",
    price_raw: 27000000,
    price_formatted: "₹2.70 Cr",
    sqft: 1613,
    floor: 3,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9b4899db59c2e019db62f051f265c/detail"
  },
  {
    id: 7,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 4 of 20)",
    price_raw: 24500000,
    price_formatted: "₹2.45 Cr",
    sqft: 1611,
    floor: 4,
    total_floor: 20,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9b57d9cff011a019cffb12f254910/detail"
  },
  {
    id: 8,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 5 of 18, 1615 sqft)",
    price_raw: 25000000,
    price_formatted: "₹2.50 Cr",
    sqft: 1615,
    floor: 5,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9be299c955359019c956c865c060c/detail"
  },
  {
    id: 9,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis, Panathur (Floor 5)",
    price_raw: 25500000,
    price_formatted: "₹2.55 Cr",
    sqft: 1611,
    floor: 5,
    total_floor: 17,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8a9faf869753208e0197533fc1e20b6f/detail"
  },
  {
    id: 10,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 7 of 18, 1613 sqft)",
    price_raw: 25500000,
    price_formatted: "₹2.55 Cr",
    sqft: 1613,
    floor: 7,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9c3779d7fc03c019d8028996223cd/detail"
  },
  {
    id: 11,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Flat In Sobha Neopolis (Floor 9 of 18)",
    price_raw: 25900000,
    price_formatted: "₹2.59 Cr",
    sqft: 1611,
    floor: 9,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa996f79ca8a486019ca950ebcd4efb/detail"
  },
  {
    id: 12,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 10 of 18)",
    price_raw: 26000000,
    price_formatted: "₹2.60 Cr",
    sqft: 1611,
    floor: 10,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9a46a9bfe7e40019bff1a15fb4646/detail"
  },
  {
    id: 13,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 11 of 21)",
    price_raw: 26000000,
    price_formatted: "₹2.60 Cr",
    sqft: 1611,
    floor: 11,
    total_floor: 21,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa99dac9d5c8fd2019d5de6c9aa2a6e/detail"
  },
  {
    id: 14,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 12 of 18)",
    price_raw: 26200000,
    price_formatted: "₹2.62 Cr",
    sqft: 1611,
    floor: 12,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9b5bc9b82e216019b830bed8612b6/detail"
  },
  {
    id: 15,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis, Balagere (Floor 12)",
    price_raw: 26500000,
    price_formatted: "₹2.65 Cr",
    sqft: 1611,
    floor: 12,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-balagere-bangalore/8a9f8a4490c3cabf0190c43d538621fa/detail"
  },
  {
    id: 16,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 12 of 18)",
    price_raw: 26500000,
    price_formatted: "₹2.65 Cr",
    sqft: 1611,
    floor: 12,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8a9faf8597ba22710197ba6c0b8224a9/detail"
  },
  {
    id: 17,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 13 of 18)",
    price_raw: 26600000,
    price_formatted: "₹2.66 Cr",
    sqft: 1611,
    floor: 13,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8a9f8a5390d3abbe0190d3b4a8dd0204/detail"
  },
  {
    id: 18,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK High Rise Flat In Sobha Neopolis (Floor 14 of 18)",
    price_raw: 27500000,
    price_formatted: "₹2.75 Cr",
    sqft: 1611,
    floor: 14,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8aa9af849f707ed7019f70f048ab2d46/detail"
  },
  {
    id: 19,
    platform: "NoBroker",
    bhk: "3 BHK",
    title: "3 BHK Premium Flat In Sobha Neopolis (Floor 14, 1615 sqft)",
    price_raw: 33000000,
    price_formatted: "₹3.30 Cr",
    sqft: 1615,
    floor: 14,
    total_floor: 18,
    link: "https://www.nobroker.in/property/buy/3-bhk-apartment-for-sale-in-panathur-bangalore/8a9f82829dcde2ef019dce6147ef1c69/detail?nbFr=carousel_premium"
  },
  {
    id: 20,
    platform: "Magicbricks",
    bhk: "3 BHK",
    title: "3 BHK 1611 Sq-ft Apartment in Sobha Neopolis Phase 1 (Floor 14)",
    price_raw: 25200000,
    price_formatted: "₹2.52 Cr",
    sqft: 1611,
    floor: 14,
    total_floor: 18,
    link: "https://www.magicbricks.com/propertyDetail/3-BHK-1611-Sq-ft-Multistorey-Apartment-FOR-Sale-Panathur-in-Bangalore-pd-4d5e6f"
  },
  {
    id: 21,
    platform: "Magicbricks",
    bhk: "3 BHK",
    title: "3 BHK 1915 Sq-ft Luxury Apartment in Sobha Neopolis (Floor 11)",
    price_raw: 29500000,
    price_formatted: "₹2.95 Cr",
    sqft: 1915,
    floor: 11,
    total_floor: 19,
    link: "https://www.magicbricks.com/propertyDetail/3-BHK-1915-Sq-ft-Sobha-Neopolis-pd-7a8b9c"
  },
  {
    id: 22,
    platform: "99acres",
    bhk: "3 BHK",
    title: "3 BHK Resale Flat in Sobha Neopolis, Higher Floor (Floor 18)",
    price_raw: 25800000,
    price_formatted: "₹2.58 Cr",
    sqft: 1611,
    floor: 18,
    total_floor: 19,
    link: "https://www.99acres.com/3-bhk-bedroom-apartment-flat-for-sale-in-sobha-neopolis-panathur-bangalore-1611-sqft-spid-Y90812"
  },
  {
    id: 23,
    platform: "99acres",
    bhk: "3 BHK",
    title: "3 BHK + 3T Large 2150 Sq-ft Flat in Sobha Neopolis (Floor 16)",
    price_raw: 33000000,
    price_formatted: "₹3.30 Cr",
    sqft: 2150,
    floor: 16,
    total_floor: 19,
    link: "https://www.99acres.com/3-bhk-2150-sqft-sobha-neopolis-spid-Z10293"
  }
];

// State Management
let currentPlatform = 'all';
let currentMinFloor = 0;
let currentSqft = 'all';
let currentSort = 'price-asc';
let currentSearch = '';
let currentView = 'cards'; // 'cards' or 'table'

document.addEventListener('DOMContentLoaded', () => {
  initDashboard();
});

function initDashboard() {
  bindEvents();
  updateKPIs();
  renderListings();
}

function bindEvents() {
  // Search input
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentSearch = e.target.value.toLowerCase();
      renderListings();
    });
  }

  // Platform Chip Buttons
  const platformChips = document.getElementById('platform-chips');
  if (platformChips) {
    platformChips.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        platformChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        e.target.classList.add('active');
        currentPlatform = e.target.dataset.platform;
        renderListings();
      });
    });
  }

  // Select Filters
  const floorSelect = document.getElementById('floor-select');
  if (floorSelect) {
    floorSelect.addEventListener('change', (e) => {
      currentMinFloor = parseInt(e.target.value, 10);
      renderListings();
    });
  }

  const sizeSelect = document.getElementById('size-select');
  if (sizeSelect) {
    sizeSelect.addEventListener('change', (e) => {
      currentSqft = e.target.value;
      renderListings();
    });
  }

  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      renderListings();
    });
  }

  // Reset Filters
  const resetBtn = document.getElementById('reset-filters');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      currentPlatform = 'all';
      currentMinFloor = 0;
      currentSqft = 'all';
      currentSort = 'price-asc';
      currentSearch = '';

      if (searchInput) searchInput.value = '';
      if (floorSelect) floorSelect.value = '0';
      if (sizeSelect) sizeSelect.value = 'all';
      if (sortSelect) sortSelect.value = 'price-asc';

      if (platformChips) {
        platformChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        platformChips.querySelector('[data-platform="all"]').classList.add('active');
      }

      renderListings();
    });
  }

  // View Mode Toggles
  const btnCards = document.getElementById('btn-view-cards');
  const btnTable = document.getElementById('btn-view-table');
  const cardsContainer = document.getElementById('listings-cards-container');
  const tableContainer = document.getElementById('listings-table-container');

  if (btnCards && btnTable) {
    btnCards.addEventListener('click', () => {
      btnCards.classList.add('active');
      btnTable.classList.remove('active');
      cardsContainer.classList.remove('hidden');
      tableContainer.classList.add('hidden');
      currentView = 'cards';
    });

    btnTable.addEventListener('click', () => {
      btnTable.classList.add('active');
      btnCards.classList.remove('active');
      tableContainer.classList.remove('hidden');
      cardsContainer.classList.add('hidden');
      currentView = 'table';
    });
  }

  // Theme Toggle
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('light-mode');
      const icon = themeToggle.querySelector('i');
      if (document.body.classList.contains('light-mode')) {
        icon.className = 'fa-solid fa-moon';
      } else {
        icon.className = 'fa-solid fa-sun';
      }
    });
  }
}

function updateKPIs() {
  const total = listingsData.length;
  const count1611 = listingsData.filter(item => item.sqft === 1611).length;
  const countHighFloor = listingsData.filter(item => item.floor >= 14).length;

  document.getElementById('stat-total-count').textContent = total;
  document.getElementById('stat-target-count').textContent = `${count1611} Listings`;
  document.getElementById('stat-highfloor-count').textContent = `${countHighFloor} Units`;
}

function getFilteredListings() {
  return listingsData.filter(item => {
    // Platform
    if (currentPlatform !== 'all' && item.platform.toLowerCase() !== currentPlatform.toLowerCase()) {
      return false;
    }
    // Floor
    if (item.floor < currentMinFloor) {
      return false;
    }
    // Sqft
    if (currentSqft !== 'all' && item.sqft !== parseInt(currentSqft, 10)) {
      return false;
    }
    // Search
    if (currentSearch) {
      const matchTitle = item.title.toLowerCase().includes(currentSearch);
      const matchPlatform = item.platform.toLowerCase().includes(currentSearch);
      const matchFloor = `floor ${item.floor}`.includes(currentSearch);
      if (!matchTitle && !matchPlatform && !matchFloor) return false;
    }
    return true;
  }).sort((a, b) => {
    if (currentSort === 'price-asc') return a.price_raw - b.price_raw;
    if (currentSort === 'price-desc') return b.price_raw - a.price_raw;
    if (currentSort === 'floor-desc') return b.floor - a.floor;
    if (currentSort === 'sqft-desc') return b.sqft - a.sqft;
    return 0;
  });
}

function renderListings() {
  const filtered = getFilteredListings();
  
  // Count Badge
  const countBadge = document.getElementById('visible-count-badge');
  if (countBadge) countBadge.textContent = `Showing ${filtered.length} of ${listingsData.length} Listings`;

  const tagIndicator = document.getElementById('active-filter-tag');
  if (tagIndicator) {
    let tagText = `Filters: Platform (${currentPlatform}), Floor (≥${currentMinFloor})`;
    if (currentSqft !== 'all') tagText += `, Area (${currentSqft} sqft)`;
    tagIndicator.textContent = tagText;
  }

  // Render Grid Cards
  const cardsContainer = document.getElementById('listings-cards-container');
  if (cardsContainer) {
    if (filtered.length === 0) {
      cardsContainer.innerHTML = `
        <div class="empty-state">
          <i class="fa-solid fa-folder-open"></i>
          <h3>No matching listings found</h3>
          <p>Try resetting filters or lowering the minimum floor restriction.</p>
        </div>
      `;
    } else {
      cardsContainer.innerHTML = filtered.map(item => {
        const ratePerSqft = Math.round(item.price_raw / item.sqft);
        const platformBadgeClass = item.platform.toLowerCase();
        
        return `
          <div class="listing-card card-glass">
            <div class="card-top-bar">
              <span class="platform-badge ${platformBadgeClass}">
                <i class="fa-solid fa-globe"></i> ${item.platform}
              </span>
              <span class="floor-badge ${item.floor >= 14 ? 'high-floor' : ''}">
                <i class="fa-solid fa-building"></i> Floor ${item.floor} / ${item.total_floor}
              </span>
            </div>

            <div class="card-main">
              <h4 class="property-title">${item.title}</h4>
              <div class="specs-pill-group">
                <span class="spec-pill"><i class="fa-solid fa-bed"></i> ${item.bhk}</span>
                <span class="spec-pill"><i class="fa-solid fa-ruler-combined"></i> ${item.sqft} sqft</span>
                <span class="spec-pill"><i class="fa-solid fa-chart-line"></i> ₹${ratePerSqft.toLocaleString('en-IN')}/sqft</span>
              </div>
            </div>

            <div class="card-bottom">
              <div class="price-box">
                <span class="price-label">Price</span>
                <h3 class="price-value">${item.price_formatted}</h3>
              </div>
              <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="btn-primary-link">
                View Listing <i class="fa-solid fa-arrow-up-right-from-square"></i>
              </a>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // Render Table View
  const tableBody = document.getElementById('table-body');
  if (tableBody) {
    tableBody.innerHTML = filtered.map(item => {
      const ratePerSqft = Math.round(item.price_raw / item.sqft);
      return `
        <tr>
          <td><span class="platform-badge ${item.platform.toLowerCase()}">${item.platform}</span></td>
          <td><strong>${item.title}</strong></td>
          <td>${item.sqft} sqft</td>
          <td><span class="badge-table-floor ${item.floor >= 14 ? 'high' : ''}">Floor ${item.floor} of ${item.total_floor}</span></td>
          <td class="price-cell">${item.price_formatted}</td>
          <td>₹${ratePerSqft.toLocaleString('en-IN')}/sqft</td>
          <td>
            <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="btn-table-action">
              View <i class="fa-solid fa-external-link"></i>
            </a>
          </td>
        </tr>
      `;
    }).join('');
  }
}
