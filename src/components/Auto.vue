<template>
  <v-container>
    <h2>Auto</h2>
    <div>
      <v-col align="center">
        <v-row>
          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field solo clearable v-model="start" placeholder="von"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field solo clearable v-model="stoppoint" placeholder="pause"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="4" cols="12">
            <v-text-field solo clearable v-model="end" placeholder="bis"></v-text-field>
          </v-col>
<!--          <v-col sm="12" xs="12" md="3" cols="12" align="left">
            <v-btn @click="search" width="100%" color="primary" dark x-large>Suchen</v-btn>
          </v-col>-->
        </v-row>
      </v-col>
      <v-row>
        <v-col align="center">
          <h4 v-if="duration1Text !== ''">{{ duration1Text }}</h4>
          <h4 v-if="stoppoint !== ''">{{ duration2Text }}</h4>
        </v-col>
      </v-row>
      <GmapMap
          style="width: 100%; height: 500px"
          :zoom="8"
          :center="{ lat: 46.8131873 , lng: 8.22421 }
      ">
        <DirectionsRenderer travelMode="DRIVING" :origin="origin" :destination="destionation" :location="location" @getDirections="getDirections" :search="search"/>
      </GmapMap>
      <v-row>
        <v-col cols="4">
          <v-list dense>
            <v-list-item>
              <v-list-item-title>
                <h2>{{ start }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip color="primary" dark>123</v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="stoppoint">
              <v-list-item-title>
                <h2>{{ stoppoint }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip color="primary" dark>213</v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>
                <h2>{{ end }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip color="primary" dark>321</v-chip>
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

  data: () => ({
    start: "Basel",
    end: "Zürich",
    stoppoint: "",
    directions: null,
    startLocation: {lat: 46.8131873, lng: 8.22421},
    endLocation: {lat: null, lng: null},
    duration1Text: "",
    duration2Text: ""
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
    getDirections (resp) {
      this.directions = resp
      //console.log(this.directions)

      this.startLocation.lat = this.directions.routes[0].legs[0].start_location.lat()
      this.startLocation.lng = this.directions.routes[0].legs[0].start_location.lng()

      this.endLocation.lat = this.directions.routes[0].legs[0].end_location.lat()
      this.endLocation.lng = this.directions.routes[0].legs[0].end_location.lng()

      this.duration = this.directions.routes[0].legs[0].duration.text
      this.distance = this.directions.routes[0].legs[0].distance.text
      this.getDistance()
    },
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
    search(){

      console.log('search pressed')
    }
  }
};
</script>

<style scoped>

</style>
