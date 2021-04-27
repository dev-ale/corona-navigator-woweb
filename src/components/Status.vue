<template>
  <v-row>
    <v-col>
      <div class="ml-5">
        <h3>Anzahl Gemeinden: {{ this.incidences.length }}</h3>
        <h3>Kantone: <strong v-for="(canton, index) in this.getCantons()" :key="index"> {{ canton }}</strong> ({{ this.getCantons().length }})</h3>
        <br>

        <h2>Aargau: 0/210</h2>
        <h2>Bern: 0/339</h2>
        <h2>Basel-Land: 86/86</h2>
        <h2>Basel-Stadt: 3/3</h2>
        <h2>Fribourg: 0/128</h2>
        <h2>Graubünden: 0/101</h2>
        <h2>Luzern: 0/80</h2>
        <h2>St. Gallen: 0/77</h2>
        <h2>Solothurn: 0/107</h2>
        <h2>Schwyz: 0/30</h2>
        <h2>Thurgau: 0/80</h2>
        <h2>Zug: 0/11</h2>
        <h2>Zürich: 0/162</h2>

      </div>
    </v-col>
    <v-col>
      <SwitzerlandMap/>
    </v-col>
  </v-row>

</template>

<script>
import SwitzerlandMap from "@/components/SwitzerlandMap";
export default {
  name: "Status",
  components: {SwitzerlandMap},
  props: {
    incidences: Array,
  },
  data: () => {
    return {

    }

  },
  mounted() {
    incidences: this.incidences
    this.getCantons();
  },
  methods: {
    getCantons() {
      let cantons = [];
      this.incidences.forEach(function (arrayItem) {
        cantons.push(arrayItem.canton)
      });
      cantons = [...new Set(cantons)];
      return cantons;
    }
  }
}
</script>

<style scoped>

</style>
