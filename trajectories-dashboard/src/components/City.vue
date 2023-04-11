<template>
    <div v-if="isDataLoaded">
            <multiselect
            :options="cities"
            v-model="selectedCity"
            track-by="id"
            label="name"
            @search-change="get_city"
            ></multiselect>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Multiselect from 'vue-multiselect'

//   Vue.component('multiselect', Multiselect)
  
  export default {
    components: {
        Multiselect
    }, 

    data() {
      return {
        cities: [],
        errors: [],
        selectedCity : null
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
        this.selectedCity = this.cities[0].id
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
     methods: {
        get_city(){
                console.log(this.selectedCity)
            }
     }


  }

  </script>