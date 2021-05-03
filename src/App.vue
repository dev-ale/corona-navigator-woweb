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

      <v-btn
          icon
          href="https://github.com/dev-ale/corona-navigator-woweb"
          target="_blank"
      >
        <v-icon>mdi-github</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

      <template v-slot:extension>
        <v-tabs align-with-title>
          <v-tab @click="view='zug'">Zug</v-tab>
          <v-tab @click="view='auto'">Auto</v-tab>
          <v-tab @click="view='status'">Status</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main style="background-color: #c44348">
      <div class="ma-12" >
        <v-card min-height="500px" height="100%">
          <v-card-text>
            <Zug v-if="view==='zug'" :incidences="incidences"/>
            <Auto v-if="view==='auto'" :incidences="incidences"/>
            <Status v-if="view==='status'" :incidences="incidences"/>
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
export default {
  name: 'App',
  components: {
    Auto,
    Status,
    Zug
  },
  data: () => ({
    view: "zug",
    incidences: [{
      name: "Basel",
      canton: "BS",
      date: "2021-04-19",
      incident: 272,
    },
      {
        name: "Muttenz",
        canton: "BS",
        date: "2021-04-19",
        incident: 222,
      },
      {
        name: "Aesch",
        canton: "BL",
        date: "2021-04-19",
        incident: 201,
      },
      {
        name: "Pratteln",
        canton: "BL",
        date: "2021-04-19",
        incident: 215,
      },
      {
        name: "Solothurn",
        canton: "SO",
        date: "2021-04-19",
        incident: 401,
      }]
  }),
  mounted() {
    this.getIncidences()
  },
/*  watch: {
    // whenever question changes, this function will run
    updateIncidences: function (newQuestion, oldQuestion) {
      this.incidences = newQuestion
      console.log('wathcer called')
    }
  },*/
  methods: {
    getIncidences() {
      axios.get(`/api/incidences`)
          .then(response => {
            // JSON responses are automatically parsed.

            console.log(response.data)
            if (response.data.length > 0) {
              console.log("Used Data from Server")
              this.incidences = response.data
            }else {
              console.log("Array is Empty")
              console.log("Sample Data used")
            }
          })
          .catch(e => {
            this.errors.push(e)
          })
    }
  }
};
</script>
