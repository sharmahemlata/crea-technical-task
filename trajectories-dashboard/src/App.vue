<script>

import moment from 'moment'
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import axios from 'axios';
import Multiselect from 'vue-multiselect'
import Map from './components/Map.vue'

export default {
        name: 'app',
        components: {
            Multiselect,
            Map,
            DatePicker
        },
        data() {
          return {
              cities: [],
              date: null,
              city: null,
              center: null,
              trajectories:[],
              queryUrl: null,
              polyline: {
                latlngs: [[47.334852, -1.509485], [47.342596, -1.328731], [47.241487, -1.190568], [47.234787, -1.358337]],
                color: 'blue'
              }
          }
        },
        computed: {
          isDataLoaded() {
              return this.cities.length != 0
          }
        
        },
        watch : {
               city:function(val) {
                if (val)
                  this.center = [this.city.geometry.latitude,this.city.geometry.longitude]
                  this.queryChanged()
               },
               date : function (val) {
                if (val)
                  this.queryChanged()
               },
               trajectories: function(val){
                console.log(this.trajectories)
                for (var i = 0; i < this.trajectories.length; i++) {
                    this.trajectories[i] = this.trajectories[i].reverse()
                }
                this.polyline.latlngs = this.trajectories
               }
        },

        mounted() {
          axios.get('https://api.energyandcleanair.org:443/cities')
          .then(response => {
            this.cities = response.data.data
            this.city = this.cities[0]
          })
          .catch(e => {
            console.error(e)
          })
        },
        methods: {
          queryChanged(data){
             if (this.date && this.city)
              this.queryUrl = 'https://api.energyandcleanair.org/v1/trajectories?location_id=' + 
                          this.city.id.replace(' ','_') + '&date=' +  moment.utc(this.date).format('YYYY-MM-DD')
                console.log(this.queryUrl)
                axios.get(this.queryUrl)
                .then(response => {
                  if (response.data.data)
                    this.trajectories = response.data.data[0].features[0].geometry.coordinates
                  else
                    console.log('No data')
                })
                .catch(e => {
                  console.error(e)
                })
          }
        }

    }
</script>

<template> 
    <div v-if="isDataLoaded" class="container">
      <div class="map">
        <Map
         :center="center"
         :polyline="polyline"
        />
      </div>
      <div class="city">
          <div>
            <multiselect
            :options="cities"
            v-model="city"
            track-by="id"
            label="name"
            ></multiselect>
          </div>
      </div>
      <div class="date">
        <div id="app">
            <div class="center">
              <date-picker v-model="date" valueType="format">{{date}}</date-picker>
            </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.container {
  display: grid;
  grid-template-columns: auto auto auto auto;
  grid-template-rows: auto auto auto;
  height: 100%;
  width: 100%;
  align-self: center;
}
 
.map{
  grid-row: 1/3;
  grid-column: 1/2;
  border: solid 2px pink;
}
.city{
  grid-row: 1/2;
  grid-column: 2/3;
  border: solid 2px green;
}

.date{
  grid-row: 1/2;
  grid-column: 3/4;
  border: solid 2px yellow;
}
.center {
        width: 50%;
        margin: 0 auto;
    }
</style>
