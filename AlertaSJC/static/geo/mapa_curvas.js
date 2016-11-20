var curvas = new ol.layer.Vector({
  title: 'curvas de nivel',
  source: new ol.source.Vector({
    url: window.curvas_URL,
    format: new ol.format.GeoJSON()
  })
});



var rio = new ol.Feature({
  geometry: new ol.geom.Point([-45.897464, -23.153995]),
  name: 'rio paraiba'
});

var vectorLayer = new ol.layer.Vector({
  source : new ol.source.Vector({
    features: [rio]
  })
});


var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }), curvas, vectorLayer
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-45.897464, -23.153995]),
    zoom: 15
  })
});
