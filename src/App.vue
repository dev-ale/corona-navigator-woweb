<template>
  <v-app>
    <v-app-bar
        app
        :color="backgroundColor"
        dark
        flat
    >
      <v-spacer></v-spacer>

      <v-app-bar-title><h2>Corona Navigator</h2></v-app-bar-title>

      <v-spacer></v-spacer>

      <v-menu
          bottom
          left
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              dark
              icon
              v-bind="attrs"
              v-on="on"
          >
            <v-icon>mdi-source-repository</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item><h4>Repositories</h4></v-list-item>
          <v-list-item href="https://github.com/dev-ale/corona-navigator-woweb" target="_blank">
            <v-list-item-avatar>
              <v-icon size="30">mdi-github</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>Frontend & Backend</v-list-item-title>
              <v-list-item-subtitle>Github</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item href="https://gitlab.fhnw.ch/wodss-wowm-group-bs-bl/webservice-bl-bs" target="_blank">
            <v-list-item-avatar>
              <v-icon size="30">mdi-gitlab</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>BS / BL Kantonsservice</v-list-item-title>
              <v-list-item-subtitle>Gitlab</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

        </v-list>
      </v-menu>

      <template v-slot:extension>
        <v-tabs v-if="!loading" align-with-title>
          <v-tab @click="view='zug'"><v-icon class="mr-5">mdi-train</v-icon>Zug</v-tab>
          <v-tab @click="view='auto'"><v-icon class="mr-5">mdi-car</v-icon>Auto</v-tab>
          <v-spacer></v-spacer>
          <v-tab class="mr-10" @click="view='status'"><v-icon class="mr-5">mdi-information-outline</v-icon>Status</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main :class="backgroundColor">
      <div class="ma-12" >
        <v-card min-height="80vh">
          <v-card-text>
            <ProgressLoader :info-text="'Fetching data from database'" v-if="loading"/>
            <div v-if="!loading">
              <Zug v-if="view==='zug'" :incidences="incidences"/>
              <Auto v-if="view==='auto'" :incidences="incidences"/>
              <Status v-if="view==='status'" :incidences="incidences"/>
            </div>
          </v-card-text>
        </v-card>
      </div>

    </v-main>

  </v-app>
</template>

<script>

import Zug from "@/components/Zug";
import Status from "@/components/Status";
import Auto from "@/components/Auto";
import ProgressLoader from "@/components/ProgressLoader";
import vuetify from "@/plugins/vuetify";


export default {
  name: 'App',
  components: {
    ProgressLoader,
    Auto,
    Status,
    Zug
  },
  data: () => ({
    loading: false,
    view: "zug",
    incidences: [],
    bgColor: "zugMain",
  }),
  mounted() {
    this.getIncidences()
  },
  computed: {
    backgroundColor: function () {
      if(this.view === "zug"){
        return "zugMain";
      }
      if (this.view === "status") {
        return "statusMain";
      }
      else {
        return "autoMain";
      }
    }
  },
  methods: {
    /*
    * Loads JSON file with all needed Data from Backend
    */
    getIncidences() {
      this.loading = true;
      axios.get(`/api/incidences`)
          .then(response => {
            if (response.data.length > 0) {
              console.log("Used data from DB")
              this.incidences = response.data
              this.loading = false;
            }else {
              console.log("Could not load from DB")
            }
          })
          .catch(e => {
            this.loading = false;
            console.log(e)
          })
    }
  }
};
</script>
