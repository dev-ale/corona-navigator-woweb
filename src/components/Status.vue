<template>
  <v-layout>
    <v-row>
      <v-col>
        <div class="ml-5">
          <h3>Gemeinden: {{ this.incidences.length }}</h3>
          <h3>Kantone: {{ this.getCantons().length }} / 13</h3>
          <br>

          <v-list >
            <v-list-item>
              <v-list-item-title>
                <h3>Kantone</h3>
              </v-list-item-title>
              <v-list-item-subtitle>
                <h3>14-Tage-Inzidenz</h3>
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-for="(canton, index) in this.getCantons()" :key="index">
              <v-list-item-title>
                <h3> {{ canton }} ({{ getCitiesForCanton(canton) }})</h3>
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
        </div>
      </v-col>
      <v-col cols="8" xs="12" md="7" align="center">
        <SwitzerlandMap @select-canton="selectCanton"/>
        <h1>{{showDetails.name}}</h1>
        <v-chip v-if="showDetails.incident" dark color="primary">{{showDetails.incident}}</v-chip>
      </v-col>
    </v-row>
  </v-layout>


</template>

<script>
import SwitzerlandMap from "@/components/SwitzerlandMap";
import Vue from "vue";
export default {
  name: "Status",
  components: {SwitzerlandMap},
  props: {
    incidences: Array,
  },
  data: () => {
    return {
      countCities: {
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
    selectCanton (canton) {
      this.showDetails.name = canton
      this.showDetails.incident = this.getIncidencesForCanton(canton)
    },

    getCantons() {
      let cantons = [];
      this.incidences.forEach(function (arrayItem) {
        cantons.push(arrayItem.canton)
      });
      cantons = [...new Set(cantons)];
      return cantons;
    },
    getDateForCanton(canton) {
      return this.incidences.filter((obj) => obj.canton === canton)[0].date;
    },
    getCitiesForCanton(canton) {
      return this.incidences.filter((obj) => obj.canton === canton).length;
    },

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
