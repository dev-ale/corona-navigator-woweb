<template>
  <v-container>
    <div>
      <AutoInput @search="search" @triggerEasterEgg="triggerEasterEgg" :incidences="incidences"/>

      <v-row v-if="!startCity.incident && !endCity.incident && !searchFail">
        <v-col align="center">
          <h2>Bitte geben Sie einen Start und Endort ein.</h2>
        </v-col>
      </v-row>

      <v-row v-if="searchFail">
        <v-col align="center">
          <NotFound message="Keine Route gefunden - Versuchen Sie es noch einmal"/>
        </v-col>
      </v-row>

      <v-row v-if="showEasterEgg">
        <v-col align="center">
          <v-img src="https://media3.giphy.com/media/Y157H6oUhV4otwNYyM/giphy.gif?cid=790b76110e29f2eef14ae59540aa9c2575501847613f0ae9&rid=giphy.gif&ct=g" max-height="60vh"  contain="true"></v-img>
        </v-col>
      </v-row>

      <v-row v-if="!showEasterEgg">
        <v-col align="center">
          <h3 v-if="duration1Text !== ''">{{ duration1Text }}</h3>
          <h3 v-if="stoptCity.address !== ''">{{ duration2Text }}</h3>
        </v-col>
      </v-row>
      <GmapMap
          class="mt-5"
          v-show="showMap"
          style="width: 100%; height: 500px"
          :zoom="8"
          :center="{ lat: 46.8131873 , lng: 8.22421 }"
      >
        <DirectionsRenderer
            travelMode="DRIVING"
            :origin="origin"
            :destination="destionation"
            :location="pause"
            @getDirections="getDirections"
            @failure="searchFailTrigger"

        />
      </GmapMap>
          <v-row v-if="startCity.incident !=null && endCity.incident != null && !searchFail && !showEasterEgg">
            <v-col xs="12" sm="12" md="4">
              <v-list dense>
                <v-list-item>
                  <v-list-item-title>
                    <h2>{{ startCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="startCity.incident != null" color="primary" dark>{{ startCity.incident }}</v-chip>
                    <v-chip v-if="startCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="stoptCity.incident">
                  <v-list-item-title>
                    <h2>{{ stoptCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="stoptCity.incident != null" color="primary" dark>{{ stoptCity.incident}}</v-chip>
                    <v-chip v-if="stoptCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <v-list-item-title>
                    <h2>{{ endCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="endCity.incident != null" color="primary" dark>{{ endCity.incident }}</v-chip>
                    <v-chip v-if="endCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
            <Score v-if="startCity.incident !=null && endCity.incident != null" :stations="stations" color="primary"/>
          </v-row>

    </div>
  </v-container>
</template>

<script>
import DirectionsRenderer from "@/components/DirectionRenderer";
import {gmapApi} from 'vue2-google-maps';
import Score from "@/components/Score";
import NotFound from "@/components/NotFound";
import AutoInput from "@/components/Auto-Input";

export default {
  components: {
    AutoInput,
    NotFound,
    DirectionsRenderer,
    Score,
  },
  props: {
    incidences: Array,
  },

  data: () => ({
    duration1Text: "",
    duration2Text: "",
    startCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
    },
    endCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
    },
    stoptCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
    },
    apikey: process.env.VUE_APP_GOOGLEMAPS_API_KEY,
    triggerSearch: -1,
    stations: [],
    searchFail: false,
    showMap: true,
    showEasterEgg: false,
  }),

  computed: {
    google: gmapApi,
    origin() {
      if (!this.startCity.address) return null;
      return {query: this.startCity.address};
    },
    destionation() {
      if (!this.endCity.address) return null;
      return {query: this.endCity.address};
    },
    pause() {
      if (!this.stoptCity.address) return null;
      return {query: this.stoptCity.address};
    },
  },
  methods: {
    /*
        * triggers failure messeage if google directions doesn't find any driections
     */
    searchFailTrigger(){
      this.searchFail = true;
      this.showMap = false;
      this.duration1Text = '';
      this.duration2Text = '';

    },
    /*
      * triggers easterEgg and disables map
    */
    triggerEasterEgg(value){
      if(value){
        this.showMap = false;
        this.showEasterEgg = true;
      }else{
        this.showMap = true;
        this.showEasterEgg = false;
      }
    },

    /*
       * changes value of triggerSearch, directions will bi rendered on change (buttonclick)
    */
    search(start, end, stoppoint){
      this.startCity = start;
      this.endCity = end;
      this.stoptCity = stoppoint;

      /*this.searchFail = false;
      if (this.startCity.address === '' || this.endCity.address === '') {
       this.searchFailTrigger()
      }else {
        this.showMap = true;
        //this.triggerSearch *= -1;
      }*/

    },
    /*
    * Get direction and display distance and duration in UI
    */
    getDirections (directions) {
      this.searchFail = false;

      this.stations = [];
      this.stations.push({name: this.startCity.name ,incident: this.startCity.incident});
      this.stations.push({name: this.stoptCity.name ,incident: this.stoptCity.incident});
      this.stations.push({name: this.endCity.name ,incident: this.endCity.incident});

      let obj1 = directions.routes[0].legs[0];
      let obj2 = directions.routes[0].legs[1];


      this.duration = directions.routes[0].legs[0].duration.text
      this.distance = directions.routes[0].legs[0].distance.text
      this.getDistance(obj1, obj2)
    },

    /*
    * Helper Function in "getDirection" to calculate and format Duration Time
    */
    getDistance (obj1, obj2) {

      let start = obj1.start_address
      let stop = obj1.end_address
      let duration = obj1.duration.text
      this.duration1Text = start + " - " + stop + " Fahrtzeit: " + duration
      if (obj2) {
        let start2 = obj2.start_address
        let stop2 = obj2.end_address
        let duration2 = obj2.duration.text
        this.duration2Text = start2 + " - " + stop2 + " Fahrtzeit: " + duration2
      }else {
        this.duration2Text = ""
      }
    },
  }
};
</script>

<style scoped>

</style>
