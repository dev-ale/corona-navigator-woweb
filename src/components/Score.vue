<template>
  <v-btn dark color="red" x-large absolute bottom right>
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
    /*
    * calculate the total incident score and get the average and round it.
    */
    calculateScore() {
      let count = 0;
      let score = 0;
      this.stations.forEach(function (arrayItem) {
        if (arrayItem.incident !== "Keine Daten verfügbar") {
          score += arrayItem.incident;
          count ++
        }
      });
      if(isNaN(score)) {
        this.score = "Keine Daten";
        return;
      }else if(score === 0)
      {
        this.score = 0;
        return;
      }
      score = score / count
      this.score = Math.round(score * 100) / 100
    }
  }
}
</script>

<style scoped>

</style>
