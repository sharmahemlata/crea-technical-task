<script>

import moment from 'moment';
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
              date: new Date().toISOString().slice(0,10),
              city: null,
              center: null,
              trajectories:[],
              queryUrl: null,
              apiResponse: null,
              polylines: [],
              message: null

          }
        },
        computed: {
          isDataLoaded() {
              return this.cities.length != 0
          },
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
                  this.date = moment.utc(val).format('YYYY-MM-DD')
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
                this.polylines = this.trajectories
               }
        },

        mounted() {
          axios.get(import.meta.env.VITE_CITIES_URL)
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
              {
                this.queryUrl = import.meta.env.VITE_TRAJECTORY_URL.replace('CITY_ID',this.city.id).replace('DATE',this.date)
                axios.get(this.queryUrl)
                .then(response => {
                  if (response.data.data)
                  {
                    this.apiResponse = response.data.data[0].features
                    this.message=null
                  }
                  else
                  {
                      this.polylines=[]
                      this.message='Data not available for ' + this.city.name + ' on ' + this.date
                  }
                })
                .catch(e => {
                  console.error(e)
                })
          }
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
      <Map :center="center" :polylines="this.polylines" />
    </div>
    <div class="two">
      <multiselect
        :options-limit="15"
        :limit="15"
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
    <div class="four">{{message}}</div>
    <div class="footer"></div>
  </div>
  <div v-else>Loading</div>
</template>

<style scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  grid-template-rows: 1fr 2fr 2fr 0.25fr;
  row-gap: 10px;
  column-gap: 30px;
}

.header {
  grid-row: 1/2;
  grid-column: 1/4;
  background-color: #d1d1e0;
  color: black;
}

.one {
  grid-row: 2/4;
  grid-column: 1/2;
}
.two {
  grid-row: 2/3;
  grid-column: 2/3;
}

.three {
  grid-row: 2/3;
  grid-column: 3/4;
}

.four {
  grid-row: 3/4;
  grid-column: 2/4;
  color: red;
}

.footer {
  grid-row: 4/5;
  grid-column: 1/4;
  background-color: #d1d1e0;
}

.heading {
  color: black;
  font-size: 40px;
  padding: auto;
  margin-top: 10px;
  margin-left: 20px;
  font-family: "Courier New", Courier, monospace;
}
</style>
