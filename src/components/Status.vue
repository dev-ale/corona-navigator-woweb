<template>
  <v-row>
    <v-col>
      <div class="ml-5">
        <h3>Gemeinden: {{ this.incidences.length }}</h3>
        <h3>Kantone: {{ this.getCantons().length }}</h3>
        <br>

        <v-list v-for="(canton, index) in this.getCantons()" :key="index">
          <v-list-item>
            <v-list-item-title>
              <h3> {{ canton }} ({{ getCitiesForCanton(canton) }})</h3>
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-chip dark color="primary">
                {{ getIncidencesForCanton(canton) }}
              </v-chip>

            </v-list-item-subtitle>
          </v-list-item>
        </v-list>



      </div>
    </v-col>
    <v-col cols="8" xs="12" md="7">
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
      }
    }

  },
  mounted() {
    //incidences: this.incidences
    this.getCantons();

  },
  methods: {
    getCantons() {
      let cantons = [];
      this.incidences.forEach(function (arrayItem) {
        cantons.push(arrayItem.canton)
        console.log(arrayItem.canton)
      });
      cantons = [...new Set(cantons)];
      console.log(cantons)
      return cantons;
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
