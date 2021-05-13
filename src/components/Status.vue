<template>
  <v-layout>
    <v-row>
      <v-col>
        <div class="ml-5">
          <h3>Gemeinden: {{ this.incidences.length }}</h3>
          <h3>Kantone: {{ this.getCantons().length }} / 13</h3>
          <br>
          <v-card>
            <v-list >

              <v-list-item>
                <v-list-item-title>
                  <h3>Kantone</h3>
                </v-list-item-title>
                <v-list-item-title>
                  <h3>Gemeinden</h3>
                </v-list-item-title>
                <v-list-item-title>
                  <h3>14-Tage-Inzidenz</h3>
                </v-list-item-title>
              </v-list-item>

              <v-list-item v-for="(canton, index) in this.getCantons()" :key="index">
                <v-list-item-avatar>
                  <v-img :src="'img/cantons/' + canton + '.jpg'"></v-img>
                </v-list-item-avatar>
                <v-list-item-title>
                  <h3> {{ canton }}</h3>
                </v-list-item-title>
                <v-list-item-title>
                  <h3>{{ getCitiesForCanton(canton) }} ({{ getTotalCitiesForCanton(canton) }})</h3>
                </v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip dark color="primary">
                    {{ getIncidencesForCanton(canton) }}
                  </v-chip>
                  <v-chip class="ml-5" small outlined color="primary">
                    {{ getDateForCanton(canton) | moment("from", "now") }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </div>
        <br>
        <div v-if="showDetails.name">
          <v-card width="400">
            <v-row>
              <v-col align="center">
                <h1>{{ showDetails.name }}</h1>
              </v-col>
            </v-row>
            <v-row>
              <v-col align="center">
                <img width="20%" :src="'img/cantons/' + showDetails.name + '.jpg'">
              </v-col>
            </v-row>
            <v-row>
              <v-col align="center">
                <v-chip x-large v-if="showDetails.incident" dark color="primary">{{showDetails.incident}}</v-chip>
              </v-col>
            </v-row>
          </v-card>
        </div>
      </v-col>
      <v-col cols="8" xs="12" md="7" align="center">
        <SwitzerlandMap @select-canton="selectCanton"/>
      </v-col>
    </v-row>
  </v-layout>
</template>

<script>
import SwitzerlandMap from "@/components/SwitzerlandMap";
export default {
  name: "Status",
  components: {
    SwitzerlandMap
  },
  props: {
    incidences: Array,
  },
  data: () => {
    return {
      totalCities: {
        AG: 210,
        BE: 339,
        BL: 86,
        BS: 3,
        FR: 128,
        GR: 101,
        LU: 80,
        SG: 77,
        SO: 107,
        SZ: 30,
        TG: 80,
        ZG: 11,
        ZH: 162
      },
      showDetails: {
        name: null,
        incident: null
      }
    }

  },
  mounted() {
    this.getCantons();

  },
  methods: {

    /*
    * Function which is called when hovering over a canton in the SVG Map
    */
    selectCanton (canton) {
      this.showDetails.name = canton
      this.showDetails.incident = this.getIncidencesForCanton(canton)
      this.selected = true
    },

    /*
    * Get all cantons without any atributes in a simple Array
    */
    getCantons() {
      let cantons = [];
      this.incidences.forEach(function (arrayItem) {
        cantons.push(arrayItem.canton)
      });
      cantons = [...new Set(cantons)];
      return cantons;
    },

    /*
    * Get the Date when from the newest incident of the canton
    */
    getDateForCanton(canton) {
      return this.incidences.filter((obj) => obj.canton === canton)[0].date;
    },

    /*
    * count all cities in the Array which matches the given canton
    */
    getCitiesForCanton(canton) {
      return this.incidences.filter((obj) => obj.canton === canton).length;
    },

    /*
    * Get the hardcoded max cities available in canton (source wikipedia)
    */
    getTotalCitiesForCanton(canton) {
      return this.totalCities.[canton];
    },

    /*
    * Get incident for given canton and round it
    */
    getIncidencesForCanton(canton) {
      let total = 0;
      const array = this.incidences.filter((obj) => obj.canton === canton)
      array.forEach(function (arrayItem) {
        total += arrayItem.incident
      });
      const count = this.getCitiesForCanton(canton)
      return Math.round(total / count)
    }
  }
}
</script>


<style scoped>

</style>
