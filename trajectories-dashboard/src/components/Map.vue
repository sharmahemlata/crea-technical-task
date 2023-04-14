<template>
  <div style="height: 90vh; width: 90vw;">
    <l-map
      ref="map"
      style="height: 90vh; width: 90vw;"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <l-polyline v-for="line in polylines" :lat-lngs="line" :color="lineColor"></l-polyline>
      <l-tile-layer :url="url"></l-tile-layer>
     </l-map>
    <div>zoom: {{zoom}}, center: {{center}}</div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LPolyline} from "vue2-leaflet";
import "leaflet/dist/leaflet.css"

export default {
  props: ['center', 'polylines'],

  components: { LMap, LTileLayer, LPolyline },

  data() {
    return {
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      zoom: 5,
      bounds: null,
      lineColor: 'blue'
    };
  },

  watch: {
     polyline: function(val){
      console.log('line changed')
     }
              
     },
  methods: {
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    centerUpdated(center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    }
  }
};
</script>