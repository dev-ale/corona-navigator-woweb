<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-spacer></v-spacer>
      <h2>fhnw pinboard - webeC</h2>
      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/dev-ale/WebEngineering"
        target="_blank"
        text
      >
        <v-icon>mdi-github</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <home/>
    </v-main>
  </v-app>
</template>

<script>


import Home from "@/views/Home";
export default {
  name: 'App',

  components: {
    Home

  },

  data: () => ({
    //
  }),
};
</script>
