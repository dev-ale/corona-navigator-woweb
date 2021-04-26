<template>
  <v-container>
    <h2>Auto</h2>
    <div>
      <v-col align="center">
        <v-row>
          <v-col sm="4" xs="4" md="3" cols="12">
            <v-text-field solo clearable v-model="start" placeholder="von"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="3" cols="12">
            <v-text-field solo clearable v-model="stoppoint" placeholder="pause"></v-text-field>
          </v-col>

          <v-col sm="4" xs="4" md="3" cols="12">
            <v-text-field solo clearable v-model="end" placeholder="bis"></v-text-field>
          </v-col>
          <v-col sm="12" xs="12" md="3" cols="12" align="left">
            <v-btn @click="search" width="100%" color="primary" dark x-large>Suchen</v-btn>
          </v-col>
        </v-row>
      </v-col>
      <GmapMap
          style="width: 100%; height: 500px"
          :zoom="8"
          :center="{ lat: 46.8131873 , lng: 8.22421 }
      ">

        <DirectionsRenderer travelMode="DRIVING" :origin="origin" :destination="destionation" :location="location" @getDirections="getDirections" :search="search"/>
        <GmapMarker
            :position="{ lat: this.startLocation.lat, lng: this.startLocation.lng}"
            :clickable="true"
            title="Test"
        />
      </GmapMap>

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
    },
    search(){

      console.log('search pressed')
    }
  }
};
</script>

<style scoped>

</style>
