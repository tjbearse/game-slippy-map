var tileSize = 256;

var MySimple = L.Util.extend({}, L.CRS.Simple, {
    // TODO may be able to replace this with a simple js map, or a step function
    scale: function (zoom) {
	/*
	if (zoom >= 4) {
	    return Math.pow(2, 2*4+zoom-4);
	} else {
	    return Math.pow(2, 2*zoom);
	}
	*/
	return Math.pow(2, zoom);
    },
    zoom: function (scale) {
	/*
	if (scale <= 256) {
	    return Math.log(scale) / (Math.LN2 * 2);
	} else {
	    return (Math.log(scale) - 8 * Math.LN2) / Math.LN2;
	}
	*/
	return Math.log(scale) / (Math.LN2);
    },
});

var map = L.map('map', {
    // TODO setup size and wrapping
    // may need my own crs? https://leafletjs.com/reference-1.3.2.html#crs-wraplng
    // this would also allow for skipping zoom layers / customizing the level
    crs: MySimple,
}).setView([-1*tileSize, 1*tileSize], 0);
L.control.mapCenterCoord().addTo(map);
var imgUrl = 'tile.png';
var tileLayer = L.tileLayer('layers/{z}/{x}.{y}.png', {
    // determined by how much we generate
    bounds: [[-2*tileSize,0], [0, 2*tileSize]],
    minZoom: -1,
    maxZoom: 6,
    // maxZoom: 4,
    maxNativeZoom: 5,
    // minNativeZoom: 0
}).addTo(map);
