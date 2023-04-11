<template>
    <div id="app">
        <div class="center">
            <Datepicker @selected="set_date" placeholder="Date">{{null}}</Datepicker>
        </div>
    </div>
</template>

<script lang="ts">
    import moment from 'moment'
    import Datepicker from 'vuejs-datepicker'

    export default {
        name: 'app',
        components: {
            Datepicker
        },
        data() {
        return {
            date: new Date()
    
        }
        },
        methods: {
            set_date(date){
                this.date = moment.utc(new Date(date)).format('YYYY-MM-DD')
                console.log(this.date)
                
            }
        }

    }
</script>

<style>
    .center {
        width: 50%;
        margin: 0 auto;
    }
</style>