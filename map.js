var tileSize = 256; // zero is half on all sides
var map = L.map('map', {
    // TODO setup size and wrapping
    // may need my own crs? https://leafletjs.com/reference-1.3.2.html#crs-wraplng
    // this would also allow for skipping zoom layers / customizing the level
    crs: L.CRS.Simple,
}).setView([0, 0], 13);
var imgUrl = 'tile.png';
var tileLayer = L.tileLayer('layers/{z}/{x}.{y}.png', {
    // determined by how much we generate
    bounds: [[-3 * tileSize, -2 * tileSize], [2 * tileSize, 3 * tileSize]], // zero is extra
    minZoom: 0,
    maxZoom: 1
}).addTo(map);
