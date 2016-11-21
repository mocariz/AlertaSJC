var styles = {
  'ch-fraca': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({
        color: 'rgba(0, 255, 0, 0.68)'
      }),
      stroke: new ol.style.Stroke({
        color: 'rgba(0, 255, 0, 0.68)',
        width: 1
      })
    })
  }),
  'ch-moderada': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({
        color: '#FFD700'
      }),
      stroke: new ol.style.Stroke({
        color: '#FFD700',
        width: 1
      })
    })
  }),
  'ch-forte': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({
        color: '#FFA500'
      }),
      stroke: new ol.style.Stroke({
        color: '#FFA500',
        width: 1
      })
    })
  }),
  'ch-muito-forte': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: new ol.style.Fill({
        color: 'red'
      }),
      stroke: new ol.style.Stroke({
        color: 'red',
        width: 1
      })
    })
  }),
  '': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 6,
      fill: null,
      stroke: new ol.style.Stroke({
        color: 'blue',
        width: 1
      })
    })
  })
}

var styleFunction = function(feature) {
  return styles[feature.getProperties()['css']];
};

var estacoes = new ol.layer.Vector({
  title: 'estacoes pluviométricas',
  source: new ol.source.Vector({
    url: window.estacoes_URL,
    format: new ol.format.GeoJSON()
  }),
  style: styleFunction
});

var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
        source: new ol.source.OSM({
            url: 'http://mt{0-3}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attributions: [
                new ol.Attribution({ html: '© Google' }),
                new ol.Attribution({ html: '<a href="https://developers.google.com/maps/terms">Terms of Use.</a>' })
            ]
        })
    }), estacoes
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-45.897464, -23.153995]),
    zoom: 11
  })
});
