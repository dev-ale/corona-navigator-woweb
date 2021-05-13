<template>
  <v-layout>
    <v-row>
      <v-col>
        <div class="ml-5">
          <h3>Gemeinden: {{ this.incidences.length }}</h3>
          <h3>Kantone: {{ this.getCantons().length }} / 13</h3>
          <br>
          <v-card v-if="!showDetails.name">
            <v-list>
              <v-list-item>
                <v-list-item-title>
                  <h4>Kantone</h4>
                </v-list-item-title>
                <v-list-item-title v-if="!$vuetify.breakpoint.mobile">
                  <h4>Gemeinden</h4>
                </v-list-item-title>
                <v-list-item-title>
                  <h4>14-Tage-Inzidenz</h4>
                </v-list-item-title>
              </v-list-item>

              <v-list-item v-for="(canton, index) in this.getCantons()" :key="index">
                <v-list-item-avatar>
                  <v-img :src="'img/cantons/' + canton + '.jpg'"></v-img>
                </v-list-item-avatar>
                <v-list-item-title>
                  <h3> {{ canton }}</h3>
                </v-list-item-title>
                <v-list-item-title v-if="!$vuetify.breakpoint.mobile">
                  <h3>{{ getCitiesForCanton(canton) }} ({{ getTotalCitiesForCanton(canton) }})</h3>
                </v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip dark color="primary">
                    {{ getIncidencesForCanton(canton) }}
                  </v-chip>
                  <v-chip v-if="!$vuetify.breakpoint.mobile" class="ml-5" small outlined color="primary">
                    {{ getDateForCanton(canton) | moment("from", "now") }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
          <div v-if="showDetails.name">
            <v-card >
              <v-row>
                <v-col align="center">
                  <h1>{{ showDetails.name }}</h1>
                </v-col>
              </v-row>
              <v-row>
                <v-col align="center">
                  <v-avatar size="100">
                    <img  :src="'img/cantons/' + showDetails.name + '.jpg'">
                  </v-avatar>
                </v-col>
              </v-row>
              <v-row>
                <v-col align="center">
                  <h4>14 Tage Inzindenz</h4>
                  <br>
                  <v-chip large v-if="showDetails.incident" dark color="primary">{{showDetails.incident}}</v-chip>
                </v-col>
              </v-row>
            </v-card>
          </div>
        </div>
        <br>
      </v-col>

<!--      Desktop Version-->
      <v-col v-if="!$vuetify.breakpoint.mobile" cols="8" xs="12" md="6" align="center">
        <SwitzerlandMap @select-canton="selectCanton" :opacity="opacity"/>
      </v-col>
<!--      Mobile Version-->
      <v-col v-if="$vuetify.breakpoint.mobile" cols="12" xs="12" md="12" align="center">
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
      },
      opacity: {
        baselstadt: null,
        baselland: null,
        aargau: null,
        bern:null,
        fribourg: null,
        graubuenden: null,
        luzern: null,
        stgallen: null,
        solothurn: null,
        schwyz: null,
        thurgau: null,
        zug: null,
        zurich: null,
      }
    }

  },
  mounted() {
    this.getCantons();
    this.calculateOpacity();
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
    * calculate Opacity for each canton MAX Value 500 Min Value 0
    */
    calculateOpacity() {
      this.opacity.baselstadt = this.normalize(this.getIncidencesForCanton('BS'),600, 0);
      this.opacity.baselland = this.normalize(this.getIncidencesForCanton('BL'),600, 0);
      this.opacity.aargau = this.normalize(this.getIncidencesForCanton('AG'),600, 0);
      this.opacity.bern = this.normalize(this.getIncidencesForCanton('BE'),600, 0);
      this.opacity.fribourg = this.normalize(this.getIncidencesForCanton('FR'),600, 0);
      this.opacity.graubuenden = this.normalize(this.getIncidencesForCanton('GR'),600, 0);
      this.opacity.luzern = this.normalize(this.getIncidencesForCanton('LU'),600, 0);
      this.opacity.stgallen = this.normalize(this.getIncidencesForCanton('SG'),600, 0);
      this.opacity.solothurn = this.normalize(this.getIncidencesForCanton('SO'),600, 0);
      this.opacity.schwyz = this.normalize(this.getIncidencesForCanton('SZ'),600, 0);
      this.opacity.thurgau = this.normalize(this.getIncidencesForCanton('TG'),600, 0);
      this.opacity.zug = this.normalize(this.getIncidencesForCanton('ZG'),600, 0);
      this.opacity.zurich = this.normalize(this.getIncidencesForCanton('ZH'),600, 0);
      console.log(this.opacity)
    },
    /*
    * Helper function to calc a normalized Number between 0-1
    * correct it with + 0.3 because opacity would be to low
    */
    normalize(val, max, min) {
      return (val - min) / (max - min) + 0.3;
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
