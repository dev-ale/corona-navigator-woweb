<template>
  <v-container>
    <h2>Auto</h2>
    <div>
      <v-col align="center">
        <v-row>
          <v-col cols="5">
            <v-text-field solo clearable v-model="start" placeholder="von"></v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field solo clearable v-model="end" placeholder="bis"></v-text-field>
          </v-col>
          <v-col cols="2" align="left">
            <v-btn @click="search" width="100%" color="primary" dark x-large>Suchen</v-btn>
          </v-col>
        </v-row>
      </v-col>
      <GmapMap
          style="width: 1150px; height: 500px"
          :zoom="7"
          :center="{ lat: 46.8131873 , lng: 8.22421 }
      ">
        <DirectionsRenderer travelMode="DRIVING" :origin="origin" :destination="destionation"/>
      </GmapMap>
    </div>
  </v-container>

</template>

<script>
import DirectionsRenderer from "@/components/DirectionRenderer";

export default {
  components: {
    DirectionsRenderer
  },

  data: () => ({
    start: "",
    end: ""
  }),

  computed: {
    origin() {
      if (!this.start) return null;
      return {query: this.start};
    },
    destionation() {
      if (!this.end) return null;
      return {query: this.end};
    }
  }
};
</script>

<style scoped>

</style>
