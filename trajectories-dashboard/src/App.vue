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

<template> 
    <!-- <div v-if="isDataLoaded">
      <div>
        <Map
         :center="center"
         :polylines="this.polylines"
        />
      </div>
      <div>
            <multiselect
            :options="cities"
            v-model="city"
            track-by="id"
            label="name"
            ></multiselect>
      </div>
      <div>
        <date-picker v-model="date" valueType="format">{{date}}</date-picker>
      </div>            
    </div> -->
    <div v-if="isDataLoaded" class="container">
      <div class="header">
        Header 
      </div>
      <div class="one">
        <Map
         :center="center"
         :polylines="this.polylines"
        />
        </div>
      <div class="two">
        <multiselect
            style="height: 20vh; width: 20vw;"
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
        Footer Here
      </div>
    </div>

</template>

<style scoped>
.container {
  display: grid;
  grid-template-columns:  1fr 2fr 2fr;
  grid-template-rows: 1fr 4fr 0.25fr;
  align-self: center;
}
 
.header{
  grid-row: 1/2;
  grid-column: 1/4;
  border: solid 2px blue;
}

.one{
  grid-row: 2/3;
  grid-column: 1/2;
  border: solid 2px pink;
}
.two{
  grid-row: 2/3;
  grid-column: 2/3;
  border: solid 2px green;
}

.three{
  grid-row: 2/3;
  grid-column: 3/4;
  border: solid 2px yellow;
}

.footer{
  grid-row: 3/4;
  grid-column: 1/4;
  border: solid 2px orange;
}


</style>
