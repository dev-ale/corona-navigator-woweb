<template>
  <v-row>
    <v-col cols="12" align="center">
      <LottieAnimation :speed="2.5" :width="300" :height="300" path="animations/covid-loader.json"/>
      <h2 class="primary--text">Loading</h2>
      <h4> {{ infoText }}</h4>
    </v-col>
  </v-row>
</template>

<script>
import LottieAnimation from "lottie-vuejs/src/LottieAnimation.vue";
export default {
name: "ProgressLoader",
  components: {
    LottieAnimation
  },
  props: {
    infoText: String
  }
}
</script>

<style scoped>

</style>
