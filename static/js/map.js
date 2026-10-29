// Leaflet Map Initialization for Store Locator
function initStoreLocatorMap(stores) {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Default center (Mumbai)
    let centerLat = 19.0760;
    let centerLng = 72.8777;

    if (stores && stores.length > 0) {
        centerLat = stores[0].lat;
        centerLng = stores[0].lng;
    }

    const map = L.map('map').setView([centerLat, centerLng], 12);

    // Free OpenStreetMap Tile Layer (No API Key Required!)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];

    // Custom Pharmacy Pin Icon
    const pharmacyIcon = L.divIcon({
        className: 'custom-pin',
        html: `<div style="background-color: #0d9488; color: white; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 2px solid white;">
                <i class="fa-solid fa-prescription-bottle-medical" style="font-size: 16px;"></i>
               </div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 34],
        popupAnchor: [0, -30]
    });

    if (stores && stores.length > 0) {
        stores.forEach(store => {
            if (store.lat && store.lng) {
                const marker = L.marker([store.lat, store.lng], { icon: pharmacyIcon }).addTo(map);
                
                const popupContent = `
                    <div style="font-family: 'Segoe UI', sans-serif; min-width: 200px;">
                        <h6 style="margin-bottom: 4px; color: #0d9488; font-weight: bold;">${store.name}</h6>
                        <p style="font-size: 12px; margin-bottom: 6px; color: #475569;">
                            <i class="fa-solid fa-location-dot text-danger"></i> ${store.address}, ${store.area}<br/>
                            <i class="fa-solid fa-phone text-primary"></i> ${store.phone}<br/>
                            <i class="fa-regular fa-clock text-muted"></i> ${store.hours || 'Open Daily'}
                        </p>
                        <div style="border-top: 1px solid #e2e8f0; padding-top: 6px; margin-top: 6px;">
                            <a href="https://www.google.com/maps/dir/?api=1&destination=${store.lat},${store.lng}" target="_blank" class="btn btn-sm btn-outline-primary w-100" style="font-size: 11px;">
                                <i class="fa-solid fa-diamond-turn-right"></i> Get Directions
                            </a>
                        </div>
                    </div>
                `;
                marker.bindPopup(popupContent);
                markers.push(marker);
            }
        });

        // Fit map bounds to show all markers
        if (markers.length > 1) {
            const group = new L.featureGroup(markers);
            map.fitBounds(group.pad(0.15));
        }
    }
}

