<script>

import moment from 'moment'
import Datepicker from 'vuejs-datepicker'
import axios from 'axios';
import Multiselect from 'vue-multiselect'
import Map from './components/Map.vue'


export default {
        name: 'app',
        components: {
            Datepicker,
            Multiselect,
            Map
        },
        data() {
          return {
              cities: [],
              date: new Date(),
              city: null,
              center:[18.5754069125,73.856068875],
              trajectories:[],
              queryUrl: null
          }
        },
        computed: {
          isDataLoaded() {
              return this.cities.length != 0
          }
        },
        mounted() {
          axios.get('https://api.energyandcleanair.org:443/cities')
          .then(response => {
            this.cities = response.data.data
            this.city = this.cities[0]
            this.center =  [this.city.geometry.latitude,this.city.geometry.longitude]
          })
          .catch(e => {
            this.errors.push(e)
          })
        },
        methods: {
          queryChanged(data){
             console.log('something-changed')
             this.queryUrl = 'https://api.energyandcleanair.org/v1/trajectories?location_id=' + 
                        this.city.id + '&date=' +  moment.utc(this.date).format('YYYY-MM-DD')
              console.log(this.queryUrl)
            //  axios.get(this.queryUrl)
            //   .then(response => {
            //     console.log(response.data)
            //   })
            //   .catch(e => {
            //     console.log(e)
            //   })
          }
        }

    }
</script>

<template> 
    <div v-if="isDataLoaded" class="container">
      <div class="map">
        <!-- <Map
         :center="center"
        /> -->
      </div>
      <div class="city">
          <div>
            <multiselect
            :options="cities"
            v-model="city"
            track-by="id"
            label="name"
            @select="queryChanged"
            ></multiselect>
          </div>
      </div>
      <div class="date">
        <div id="app">
            <div class="center">
                <Datepicker v-model="date"/>
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
