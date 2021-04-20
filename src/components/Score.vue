<template>
  <v-btn color="primary" x-large outlined absolute bottom right>
    <h3>Score: {{ score }}</h3>
  </v-btn>
</template>

<script>
export default {
  name: "Score",
  props: {
    stations: Array,
  },
  watch: {
    stations: function (newVal, oldVal) { // watch it
      this.calculateScore();
    }
  },
  data: () => ({
    score: null

  }),
  mounted() {
    this.calculateScore()
  },
  methods: {
    calculateScore() {
      let count = 0;
      let score = 0;
      this.stations.forEach(function (arrayItem) {
        if (arrayItem.incident !== "Keine Daten verfügbar") {
          score += arrayItem.incident;
          count ++
        }
      });
      score = score / count
      this.score = Math.round(score * 100) / 100
    }
  }
}
</script>

<style scoped>

</style>
