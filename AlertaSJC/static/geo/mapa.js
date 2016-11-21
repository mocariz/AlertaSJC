var styles = {
  'vigilancia': new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'rgba(0, 255, 0, 0.68)',
      width: 3
    })
  }),
  'atencao': new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#FFD700',
      width: 3
    })
  }),
  'alerta': new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#FFA500',
      width: 3
    })
  }),
  'prontidao': new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'red',
      width: 3
    })
  })
}

var styleFunction = function(feature) {
  return styles[feature.getProperties()['css']];
};

var cotas = new ol.layer.Vector({
  title: 'cotas',
  source: new ol.source.Vector({
    url: window.cotas_URL,
    format: new ol.format.GeoJSON()
  }),
  style: styleFunction
});

var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }), cotas
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-45.897464, -23.153995]),
    zoom: 15
  })
});
