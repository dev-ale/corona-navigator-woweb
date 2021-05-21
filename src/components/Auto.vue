<template>
  <v-container>
    <div>
      <v-col align="center">
        <v-row>
          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field @keyup.enter="search" solo clearable v-model="start" placeholder="von"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field @keyup.enter="search" solo clearable v-model="stoppoint" placeholder="pause"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field @keyup.enter="search" solo clearable v-model="end" placeholder="bis"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn @click="search" width="100%" outlined color="primary" dark x-large>Suchen</v-btn>
          </v-col>
        </v-row>
      </v-col>

      <v-row v-if="!startCity.incident && !endCity.incident">
        <v-col align="center">
          <h2>Bitte geben Sie einen Start und Endort ein.</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col align="center">
          <h4 v-if="duration1Text !== ''">{{ duration1Text }}</h4>
          <h4 v-if="stoppoint !== ''">{{ duration2Text }}</h4>
        </v-col>
      </v-row>
      <GmapMap
          style="width: 100%; height: 500px"
          :zoom="8"
          :center="{ lat: 46.8131873 , lng: 8.22421 }"
      >
        <DirectionsRenderer
            travelMode="DRIVING"
            :origin="start"
            :destination="end"
            :location="stoppoint"
            :count="triggerSearch"
            @getDirections="getDirections"

        />
      </GmapMap>
          <v-row v-if="startCity.incident !=null && endCity.incident != null">
            <v-col xs="12" sm="12" md="4">
              <v-list dense>
                <v-list-item>
                  <v-list-item-title>
                    <h2>{{ startCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="startCity.incident != null" color="primary" dark>{{ checkAndRound(startCity.incident) }}</v-chip>
                    <v-chip v-if="startCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="stoptCity.incident">
                  <v-list-item-title>
                    <h2>{{ stoptCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="stoptCity.incident != null" color="primary" dark>{{ checkAndRound(stoptCity.incident)}}</v-chip>
                    <v-chip v-if="stoptCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <v-list-item-title>
                    <h2>{{ endCity.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip v-if="endCity.incident != null" color="primary" dark>{{ checkAndRound(endCity.incident)}}</v-chip>
                    <v-chip v-if="endCity.incident === null" outlined color="primary">Loading!</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
    </div>
  </v-container>
</template>

<script>
import DirectionsRenderer from "@/components/DirectionRenderer";
import {gmapApi} from 'vue2-google-maps'

export default {
  components: {
    DirectionsRenderer
  },
  props: {
    incidences: Array,
  },

  data: () => ({
    start: "",
    end: "",
    stoppoint: "",
    duration1Text: "",
    duration2Text: "",
    startCity: {
      name: "",
      incident :null
    },
    endCity: {
      name: "",
      incident :null
    },
    stoptCity: {
      name: "",
      incident :null
    },
    apikey: process.env.VUE_APP_GOOGLEMAPS_API_KEY,
    triggerSearch: -1,

  }),

  computed: {
    google: gmapApi,
  },
  methods: {
    /*
       * changes value of triggerSearch, directions will bi rendered on change (buttonclick)
    */
    checkAndRound(incident){
      if(incident){
        return incident
      }else{
        return Math.round(incident);
      }
    },
    /*
       * changes value of triggerSearch, directions will bi rendered on change (buttonclick)
    */
    search(){
      this.triggerSearch *= -1;
    },
    /*
      * corrects some wrong values given by google api
    */
    correctCityName(city){
      if (city.long_name.includes("Sankt")) {
        return city.long_name.replace("Sankt", "St.")
      }else if(city.long_name.includes("Biel")){
        return city.long_name.concat("/Bienne")
      }else if(city.long_name.includes("Kanton Reinach")){
        return city.long_name.replace("Kanton ", "")
      } else {return city.long_name;}
    },
    /*
       * Calculate  Incident for specific lng and lat from city and return the incident value
    */
    async getIncidentsByCoordinates(lng, lat) {
      return await axios.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lng + "&key=" +this.apikey)
          .then(response => {
            //placeholder for cityname and canton
            let m = {};
            let cityname;
            let canton;
            //Set placeholder cityname and canton
            response.data.results[0].address_components.forEach(x => {
                  if (x.types.includes("locality")) {
                    //correcting naming from Google api
                    cityname = this.correctCityName(x);
                  } else if (x.types.includes("administrative_area_level_1")) {
                    canton = x.short_name;
                  }
                }
            )
            //search for City in our database and fils array with cityname and the corrisponding incident
            const city = this.incidences.find(v => v.name === cityname && v.canton === canton);
            if (city != undefined) {
              m = {name: city.name, incident: city.incident}
            } else {
              m = {name: cityname, incident: "Keine Daten verfügbar"}
              //logs all city which weren't found in our database
              console.log(cityname, canton)
            }
            return m;
          }).catch(e => console.log(e));
    },

    /*
    * Get direction and display distance and duration in UI
    */
    getDirections (directions) {
      this.stoptCity = {
        name: "",
        incident :null
      }
      let startLocation = {lat: null, lng: null};
      let stopLocation = {lat: null, lng: null};
      let endLocation= {lat: null, lng: null};



      let obj1 = directions.routes[0].legs[0];
      let obj2 = directions.routes[0].legs[1];

      startLocation.lat = obj1.start_location.lat();
      startLocation.lng = obj1.start_location.lng();

      if(obj2){
        endLocation.lat = obj2.end_location.lat();
        endLocation.lng = obj2.end_location.lng();

        stopLocation.lat = obj2.start_location.lat();
        stopLocation.lng = obj2.start_location.lng();

        this.getIncidentsByCoordinates(stopLocation.lng, stopLocation.lat).then(m => {
          this.stoptCity = m;
        })

      }else{
        endLocation.lat = directions.routes[0].legs[0].end_location.lat()
        endLocation.lng = directions.routes[0].legs[0].end_location.lng()
      }

      this.getIncidentsByCoordinates(startLocation.lng, startLocation.lat).then(m => {
        this.startCity = m;
      })
      this.getIncidentsByCoordinates(endLocation.lng, endLocation.lat).then(m => {
        this.endCity = m;
      })


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
