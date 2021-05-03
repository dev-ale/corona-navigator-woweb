<template>
  <v-container>
    <ZugInput @search="search"/>
    <v-row v-if="!notFound && !stations && !loading">
      <v-col align="center">
        <h2>Bitte geben Sie einen Start und Endort ein.</h2>
      </v-col>
    </v-row>

    <ZugStationNotFound v-if="notFound" :message="message"/>
    <ZugStations v-if="!loading" :stations="stations"/>
    <Score v-if="stations" :stations="stations"/>
    <ProgressLoader v-if="loading"/>
  </v-container>
</template>

<script>
import Score from "@/components/Score";
import ProgressLoader from "@/components/ProgressLoader";
import ZugStations from "@/components/Zug-Stations";
import ZugInput from "@/components/Zug-Input";
import ZugStationNotFound from "@/components/ZugStationNotFound";
export default {
  name: "Zug",
  components: {ZugStationNotFound, ZugInput, ZugStations, ProgressLoader, Score},
  props: {
    incidences: Array,
  },
  data: () => ({
    from: "Pratteln",
    to: "Basel",
    loading: false,
    stations: null,
    score: null,
    message: null,
    notFound: false
  }),
  mounted() {
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
    search(from,to) {
      this.notFound = false
      this.loading = true
      this.message = null
      var self = this
      axios.get(`https://transport.opendata.ch/v1/connections?from=${from}&to=${to}&limit=1`)
          .then(response => {
            //console.log(response)
            let sections = [];
            let passList = [];
            let stations = [];

            // Check if response is empty
            if (response.data.connections.length === 0) {
              this.notFound = true
              this.stations = null
              this.message = 'We could not find a route for your start and end position'
              this.loading = false
            }else {
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
            }

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
