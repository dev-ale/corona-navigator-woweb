<template>
  <v-app>
    <v-app-bar
        app
        color="primary"
        dark
        flat
    >


      <v-spacer></v-spacer>

      <v-app-bar-title><h2>Corona Navigator</h2></v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-github</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

      <template v-slot:extension>
        <v-tabs align-with-title>
          <v-tab>Zug</v-tab>
          <v-tab>Auto</v-tab>
          <v-tab>Status</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main style="background-color: #c44348">
      <div class="ma-12" >
        <v-card height="700">

        </v-card>

      </div>

    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  data: () => ({
    incidences: [{
      timeStamp: "timestamp",
      name: "Basel",
      canton: "BS",
      date: "2021-04-19",
      incident: "272",
    },
      {
        timeStamp: "timestamp",
        name: "Aesch",
        canton: "BL",
        date: "2021-04-19",
        incident: "201",
      }]
  }),
};
</script>
