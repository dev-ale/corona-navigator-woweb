<template>
  <div>
    <v-col align="center">
      <v-row>
        <v-col cols="5">
          <v-text-field solo clearable v-model="from" placeholder="von"></v-text-field>
        </v-col>
        <v-col cols="5">
          <v-text-field solo clearable v-model="to" placeholder="bis"></v-text-field>
        </v-col>
        <v-col cols="2" align="left">
          <v-btn @click="search" width="100%" color="primary" dark x-large>Suchen</v-btn>
        </v-col>
      </v-row>
    </v-col>

    <v-row>
      <v-col cols="4">
        <v-list dense v-for="station of stations" :key="station.name">
          <v-list-item>
            <v-list-item-title>
              <h2>{{ station.name }}</h2>
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-chip v-if="!isNaN(station.incident)"color="primary" dark>{{ station.incident }}</v-chip>
              <v-chip v-if="isNaN(station.incident)" outlined color="primary" dark>{{ station.incident }}</v-chip>
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
    <Score v-if="stations" :stations="stations"/>
  </div>
</template>

<script>
import Score from "@/components/Score";
export default {
  name: "Zug",
  components: {Score},
  props: {
    incidences: Array,
  },
  data: () => ({
    from: "Pratteln",
    to: "Basel",
    loading: false,
    stations: null,
    score: null

  }),
  mounted() {
    incidences: this.incidences
  },

  methods: {

    // Calculalate Incidents from city name
    getIncident(n) {
      let name = n.charAt(0).toUpperCase() + n.slice(1);
      if (this.incidences.find(it => it.name === name)) {
        const city = this.incidences.find(it => it.name === name);
        return (city.incident)
      }else {
        return "Keine Daten verfügbar"
      }

    },
    // Transport Opendata API Call
    search() {
      this.loading = true
      var self = this
      axios.get(`https://transport.opendata.ch/v1/connections?from=${this.from}&to=${this.to}&limit=1`)
          .then(response => {
            console.log(response)
            let sections = [];
            let passList = [];
            let stations = [];

            sections = response.data.connections[0].sections;
            sections.forEach(function (arrayItem) {
              if (arrayItem.journey) {
                passList = arrayItem.journey.passList;
                passList.forEach(function (arrayItem2) {

                  // remove everything after comma
                  let name = arrayItem2.station.name.split(',')[0]

                  // Separate Stations with 2 Cities in it
                  let name2;
                  if (name.includes('-')) {
                    name = arrayItem2.station.name.split('-')[0]
                    name2 = arrayItem2.station.name.split('-')[1]
                  }
                  // if SBB at the end remove it
                  if (name.endsWith(" SBB")) {
                    name = arrayItem2.station.name.split(' ')[0]
                  }
                  // if HB at the end remove it
                  if (name.endsWith(" HB")) {
                    name = arrayItem2.station.name.split(' ')[0]
                  }
                  // if HB at the end remove it
                  if (name.endsWith(" Dreispitz")) {
                    name = arrayItem2.station.name.split(' ')[0]
                  }
                  // other Filters
                  if (name.endsWith("tunnel") || name.endsWith("Strecke") || name === "Gotthard" || name === "Basistunnel" || name === "Bahn" || name === "2000" || name === "Basistunnel") {
                  }
                  let incident = self.getIncident(name)
                  stations.push({name: name, incident: incident})

                  if (name2) {
                    let incident2 = self.getIncident(name2);
                    stations.push({name: name2, incident: incident2})
                  }
                  stations = stations.filter((v,i,a)=>a.findIndex(t=>(t.name === v.name))===i)
                })
              }
            });
            // Drop duplicates
            this.stations = [...new Set(stations)];
            //this.stations = stations

            this.loading = false
          })
          .catch(e => {
            console.log(e)
          })
    }
  },


}
</script>

<style scoped>

</style>
