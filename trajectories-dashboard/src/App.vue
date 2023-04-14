<script>

import moment from 'moment'
import DatePicker from 'vue2-datepicker';
import axios from 'axios';
import Multiselect from 'vue-multiselect'
import Map from './components/Map.vue'

import 'vue2-datepicker/index.css';

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
              date: new Date(),
              city: null,
              center: null,
              trajectories:[],
              queryUrl: null,
              apiResponse: null,
              polylines: []

          }
        },
        computed: {
          isDataLoaded() {
              return this.cities.length != 0
          }
        
        },
        watch : {
               city:function(val) {
                if (val){
                  this.center = [this.city.geometry.latitude,this.city.geometry.longitude]
                  this.queryChanged()
                }

               },
               date : function (val) {
                if (val){
                  this.queryChanged()
                }
               },
               apiResponse: function(val){
                this.trajectories = []
                for(var i=0; i < this.apiResponse.length ; i++){
                  
                  for (var j=0; j<this.apiResponse[i].geometry.coordinates.length;j++){
                    this.apiResponse[i].geometry.coordinates[j] = this.apiResponse[i].geometry.coordinates[j].reverse()
                  }
                  this.trajectories.push(this.apiResponse[i].geometry.coordinates)
                }
                console.log(this.trajectories.length)                
                this.polylines = this.trajectories
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
                  {
                    this.apiResponse = response.data.data[0].features
                  }
                  else
                  {
                      console.log('No data')
                  }
                })
                .catch(e => {
                  console.error(e)
                })
          }
        }

    }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<template> 
    <div v-if="isDataLoaded" class="container">
      <div class="header">
        <h1 class="heading">Air Trajectories Dashboard</h1>
      </div>
      <div class="one">
        <Map
         :center="center"
         :polylines="this.polylines"
        />
        </div>
      <div class="two">
        <multiselect
            :options-limit="10"
            :options="cities"
            v-model="city"
            track-by="id"
            label="name"
            placeholder="City"
            ></multiselect>
      </div>
      <div class="three">
        <date-picker 
        v-model="date" 
        valueType="format"
        placeholder="Date"
        ></date-picker>
      </div>
      <div class="footer">
      </div>
    </div>
    <div v-else>Loading</div>
</template>

<style scoped>
.container {
  display: grid;
  grid-template-columns:  1fr 2fr 2fr;
  grid-template-rows: 1fr 4fr 0.25fr;
  row-gap: 10px;
  column-gap: 50px;
  align-self: center;
}
 
.header{
  grid-row: 1/2;
  grid-column: 1/4;
  background-color:  #d1d1e0;
}

.one{
  grid-row: 2/3;
  grid-column: 1/2;
}
.two{
  grid-row: 2/3;
  grid-column: 2/3;
}

.three{
  grid-row: 2/3;
  grid-column: 3/4;
}

.footer{
  grid-row: 3/4;
  grid-column: 1/4;
  background-color:  #d1d1e0;
}

</style>
