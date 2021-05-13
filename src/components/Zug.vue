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
  components: {
    ZugStationNotFound,
    ZugInput,
    ZugStations,
    ProgressLoader,
    Score
  },
  props: {
    incidences: Array,
  },
  data: () => ({
    from: "",
    to: "",
    loading: false,
    stations: null,
    order: [],
    score: null,
    message: null,
    notFound: false,
    apikey: process.env.VUE_APP_GOOGLEMAPS_API_KEY
  }),
  mounted() {
  },

  methods: {

    /*
    * Calculate  Incident for specific city and return the incident value
    */
    getIncident(n) {
      const name = n.charAt(0).toUpperCase() + n.slice(1);
      if (this.incidences.find(it => it.name === name)) {
        const city = this.incidences.find(it => it.name === name);
        return (city.incident)
      } else {
        return null
      }

    },

    /*
    * Open Transport API Call to get Train Stations between Start and Stop
    */
    //Todo: @Pascal bitte noch Funktionsvariabeln ändern und Function beschriften
    search(from, to) {
      this.notFound = false
      this.loading = true
      this.message = null
      this.stations = []
      axios.get(`https://transport.opendata.ch/v1/connections?from=${from}&to=${to}&limit=1`)
          .then(response => {
            console.log(response)
            let sections = [];
            let something = [];
            this.order = [];
            this.stations = [];

            // Check if response is empty
            if (response.data.connections.length === 0) {
              this.notFound = true
              this.stations = []
              this.message = 'We could not find a route for your start and end position'
              this.loading = false
            } else {
              sections = response.data.connections[0].sections;
              let newlist = sections.map(x => {
                if (x.journey && x.journey.passList) {
                  return x.journey.passList.map(y => y.station.coordinate)
                } else {
                  return null;
                }
              });
              newlist.forEach(l => {
                if (l) {
                  l.forEach(e => this.order.push((e)))
                }
              });
              let promises = [];
              this.order.forEach((c,index) => {
                promises.push(
                 axios.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + c.x + "," + c.y + "&key=" +this.apikey )
                    .then(response => {
                      let dorf;
                      let canton;
                      response.data.results[0].address_components.forEach(x => {
                            if (x.types.includes("locality")) {
                              if (x.long_name.includes("Sankt")) {
                                dorf = x.long_name.replace("Sankt", "St.")
                              }else if(x.long_name.includes("Biel")){
                                dorf = x.long_name.concat("/Bienne")
                              }else {dorf = x.long_name;}
                            } else if (x.types.includes("administrative_area_level_1")) {
                              canton = x.short_name;
                            }
                          }
                      )
                      const d = this.incidences.find(v => v.name === dorf && v.canton === canton);
                      if (d != undefined) {
                        something[index] = ({name: d.name, incident: d.incident})
                      } else {
                        something[index] = ({name: dorf, incident: "Keine Daten verfügbar"})
                        console.log(dorf, canton)
                      }
                    })
                )
              });
              Promise.all(promises).then(() => {
                let somethingnew = something.filter(function (el) {
                  return el != null;
                })
                somethingnew = somethingnew.filter( (value, index, self) => {
                  if(self[index + 1] !== undefined) {
                      return self[index+1].name !== value.name;
                  }else return true;
                });
                this.stations = [...new Set(somethingnew)];
                this.loading = false;
              });
            }
          })
          .catch(e => {
            console.log(e)
          })
    }
  }
}
</script>

<style scoped>

</style>
