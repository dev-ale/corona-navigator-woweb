<template>
  <v-row>
    <v-col align="center">
      <LottieAnimation :loop="false" :width="300" :height="300" path="animations/not-found.json"/>
      <h2>{{ message }}</h2>
    </v-col>
  </v-row>
</template>

<script>
import LottieAnimation from "lottie-vuejs/src/LottieAnimation.vue";

export default {
name: "ZugStationNotFound",
  components: { LottieAnimation },
  props: {
    message: String,
  },
}

</script>

<style scoped>

</style>
