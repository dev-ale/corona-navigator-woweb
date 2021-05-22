<template>
  <v-container>
    <ZugInput v-if="!stations" @search="search"/>
    <v-col v-if="stations && !loading" align="center">
      <v-row>
        <v-col sm="4" xs="4" md="4" cols="12" align="left">
          <v-btn max-width="120" @click="stations = null" width="100%" outlined color="zugMain" dark large>Zurück</v-btn>
        </v-col>
      </v-row>
    </v-col>

    <v-row v-if="!notFound && !stations && !loading">
      <v-col align="center">
        <h2>Bitte geben Sie einen Start und Endort ein.</h2>
      </v-col>
    </v-row>

    <NotFound v-if="notFound" :message="message"/>

    <ZugStations v-if="!notFound && !loading && stations" :stations="stations" :departure="departure" :arrival="arrival"/>

    <Score v-if="!notFound && !loading && stations" :stations="stations" color="red"/>

    <ProgressLoader v-if="loading"/>
  </v-container>
</template>

<script>
import Score from "@/components/Score";
import ProgressLoader from "@/components/ProgressLoader";
import ZugStations from "@/components/Zug-Stations";
import ZugInput from "@/components/Zug-Input";
import NotFound from "@/components/NotFound";

export default {
  name: "Zug",
  components: {
    NotFound,
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
    filteredCoordinates: [],
    score: null,
    message: null,
    notFound: false,
    apikey: process.env.VUE_APP_GOOGLEMAPS_API_KEY,

    departure: {
      name: null,
      time: null,
      type: null
    },
    arrival: {
      name: null,
      time: null,
      type: null
    },
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
    * correcting some found issues with wrong naming
    * example: Googe api returns "Biel", our database has "Biel/Bienne" deposited
    * this function expans "Biel" with "/Bienne"
    */
    correctCityName(city){
      if (city.long_name.includes("Sankt")) {
        return city.long_name.replace("Sankt", "St.")
      }else if(city.long_name.includes("Biel")){
        return city.long_name.concat("/Bienne")
      }else {return city.long_name;}
    },
    /*
    * Open Transport API Call to get Train Stations between Start and Stop
    */
    search(from, to) {
      this.notFound = false
      this.loading = true
      this.message = null
      this.stations = []
      axios.get(`https://transport.opendata.ch/v1/connections?from=${from}&to=${to}&limit=1`)
          .then(response => {
            let sections = [];
            let stops = [];
            this.filteredCoordinates = [];
            this.stations = [];
            if (!from || !to) {
              this.notFound = true
              this.stations = []
              this.message = 'Bitte geben Sie eine gültige Start und Endposition ein'
              this.loading = false
              this.stations = null
            }
            // Check if response is empty
            else if (response.data.connections.length === 0) {
              this.notFound = true
              this.stations = []
              this.message = 'Wir konnten keine Route für diese Start und Endposition finden'
              this.loading = false
              this.stations = null
            } else {
              //get coordinates of stops from respond
              this.departure.name = response.data.from.name;
              this.departure.time = response.data.connections[0].from.departure.slice(11,16);
              this.departure.type = response.data.connections[0].products[0];

              this.arrival.name = response.data.to.name;
              this.arrival.time = response.data.connections[0].to.arrival.slice(11,16);
              const lastEl = response.data.connections[0].products.length -1;
              this.arrival.type = response.data.connections[0].products[lastEl];

              sections = response.data.connections[0].sections;
              let coordinates = sections.map(x => {
                if (x.journey && x.journey.passList) {
                  return x.journey.passList.map(y => ({c: y.station.coordinate, ar: y.arrival, dep: y.departure}))
                } else {
                  return null;
                }
              });
              //filter coordinate and pushed in one dimensional array
              coordinates.forEach(l => {
                if (l) {
                  l.forEach(e => this.filteredCoordinates.push((e)))
                }
              });
              this.filteredCoordinates = this.filteredCoordinates.filter(x => x.ar || x.dep)
                                                                  .map(x => x.c);


              //array for promises from google api get request
              let promises = [];
              //search search for Cityname and Canton with google api
              this.filteredCoordinates.forEach((c,index) => {
                //push every get rquest in promises array
                promises.push(
                  //actual get request to google api
                 axios.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + c.x + "," + c.y + "&key=" +this.apikey )
                    .then(response => {
                      //placeholder for cityname and canton
                      let cityname;
                      let canton;
                      //Set placeholder cityname and canton
                      response.data.results[0].address_components.forEach(x => {
                            if (x.types.includes("locality")) {
                              //correcting naming from Google api
                              cityname =this.correctCityName(x);
                            } else if (x.types.includes("administrative_area_level_1")) {
                              canton = x.short_name;
                            }
                          }
                      )
                      //search for City in our database and fils array with cityname and the corrisponding incident
                      const city = this.incidences.find(v => v.name === cityname && v.canton === canton);
                      if (city != undefined) {
                        stops[index] = ({name: city.name, incident: city.incident})
                      } else {
                        stops[index] = ({name: cityname, incident: "Keine Daten verfügbar"})
                        //logs all city which weren't found in our database
                        //console.log(cityname, canton)
                      }
                    }).catch(e => console.log(e))
                )
              });
              //waits for all promises => so all stations are in array
              Promise.all(promises).then(() => {
                //filters all null elements in array
                stops = stops.filter((el) => {
                  return el != null;
                })
                //filters multiple occurrences of city
                stops = stops.filter( (value, index, self) => {
                  if(self[index + 1] !== undefined) {
                      return self[index+1].name !== value.name;
                  }else return true;
                });
                //pushed everything as a set in stations array
                this.stations = [...new Set(stops)];
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
  .anzeigetafel {
    background-color: #2B42BF;
    color: white;
    padding: 10px;
    padding-bottom: 30px;
    padding-left: 20px;
    border-color: #021749;
    border-radius: 4px;
    border-style: solid;
    border-width: 6px;
    font-family: 'Arial Black';
  }


</style>
