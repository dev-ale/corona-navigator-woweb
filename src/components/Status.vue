<template>
  <v-row>
    <v-col>
      <div class="ml-5">
        <h3>Anzahl Gemeinden: {{ this.incidences.length }}</h3>
        <h3>Kantone: <strong v-for="(canton, index) in this.getCantons()" :key="index"> {{ canton }}</strong> ({{ this.getCantons().length }})</h3>
      </div>
    </v-col>
  </v-row>

</template>

<script>
export default {
  name: "Status",
  props: {
    incidences: Array,
  },
  data: () => {
    return {
      incidences: this.incidences
    }

  },
  mounted() {
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
