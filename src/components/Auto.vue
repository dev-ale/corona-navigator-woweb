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
            :origin="origin"
            :destination="destionation"
            :location="location"
            :count="count"
            @getDirections="getDirections"

        />
      </GmapMap>
      <v-row v-if="startCity.incident && endCity.incident">
        <v-col xs="12" sm="12" md="4">
          <v-list dense>
            <v-list-item>
              <v-list-item-title>
                <h2>{{ startCity.name }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip v-if="this.startCity.incident != null" color="primary" dark>{{ this.startCity.incident }}</v-chip>
                <v-chip v-if="this.startCity.incident === null" outlined color="primary">Loading!</v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="stoptCity.incident">
              <v-list-item-title>
                <h2>{{ stoptCity.name }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip v-if="this.stoptCity.incident != null" color="primary" dark>{{ this.stoptCity.incident}}</v-chip>
                <v-chip v-if="this.stoptCity.incident === null" outlined color="primary">Loading!</v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>
                <h2>{{ endCity.name }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip v-if="this.endCity.incident != null" color="primary" dark>{{ this.endCity.incident}}</v-chip>
                <v-chip v-if="this.endCity.incident === null" outlined color="primary">Loading!</v-chip>
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
    directions: null,
    startLocation: {lat: null, lng: null},
    stopLocation: {lat: null, lng: null},
    endLocation: {lat: null, lng: null},
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
    count: -1,

  }),

  computed: {
    google: gmapApi,
    origin() {
      if (!this.start) return null;
      return {query: this.start};
    },
    destionation() {
      if (!this.end) return null;
      return {query: this.end};
    },
    location() {
      if (!this.stoppoint) return null;
      return this.stoppoint;
    }
  },
  methods: {

    search(){
      this.count *= -1;
    },
    /*
    * Calculate  Incident for specific city and return the incident value
    */
    getIncident(cityName) {
      const name = cityName.charAt(0).toUpperCase() + cityName.slice(1);
      if (this.incidences.find(it => it.name === name)) {
        const city = this.incidences.find(it => it.name === name);
        return (city.incident)
      } else {
        return "Keine Daten verfügbar"
      }
    },

    correctCityName(city){
      if (city.long_name.includes("Sankt")) {
        return city.long_name.replace("Sankt", "St.")
      }else if(city.long_name.includes("Biel")){
        return city.long_name.concat("/Bienne")
      }else {return city.long_name;}
    },

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
    getDirections (resp) {
      this.startCity, this.stoptCity, this.endCity = {
        name: "",
        incident :null
      }

      this.directions = resp
      let obj1 = this.directions.routes[0].legs[0];
      let obj2 = this.directions.routes[0].legs[1];

      console.log(this.directions);
      this.startLocation.lat = obj1.start_location.lat();
      this.startLocation.lng = obj1.start_location.lng();

      if(obj2){
        this.endLocation.lat = obj2.end_location.lat();
        this.endLocation.lng = obj2.end_location.lng();

        this.stopLocation.lat = obj2.start_location.lat();
        this.stopLocation.lng = obj2.start_location.lng();

        this.getIncidentsByCoordinates(this.stopLocation.lng, this.stopLocation.lat).then(m => {
          this.stoptCity = m;
        })

      }else{
        this.endLocation.lat = this.directions.routes[0].legs[0].end_location.lat()
        this.endLocation.lng = this.directions.routes[0].legs[0].end_location.lng()
      }
      this.getIncidentsByCoordinates(this.startLocation.lng, this.startLocation.lat).then(m => {
        this.startCity = m;
      })
      this.getIncidentsByCoordinates(this.endLocation.lng, this.endLocation.lat).then(m => {
        this.endCity = m;
        console.log(this.endCity);
      })


      this.duration = this.directions.routes[0].legs[0].duration.text
      this.distance = this.directions.routes[0].legs[0].distance.text
      this.getDistance()



    },

    /*
    * Helper Function in "getDirection" to calculate and format Duration Time
    */
    getDistance () {
      let obj1 = this.directions.routes[0].legs[0]
      let obj2 = this.directions.routes[0].legs[1]

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
