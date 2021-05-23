<template>
  <v-col align="center">
    <v-row>
      <v-col sm="4" xs="4" md="4" cols="12">
        <gmap-autocomplete
            placeholder="Von"
            @place_changed="(place) => {setStart(place); search()}"
            class="InputField"
            :select-first-on-enter="true">
        </gmap-autocomplete>
      </v-col>

      <v-col sm="4" xs="4" md="4" cols="12">
          <gmap-autocomplete
              placeholder="Pause"
              @place_changed="(place) => {setPause(place); search()}"
              class="InputField"
              :select-first-on-enter="true">
          </gmap-autocomplete>
      </v-col>

      <v-col sm="4" xs="4" md="4" cols="12">
          <gmap-autocomplete
              placeholder="Bis"
              @place_changed="(place) => {setEnd(place); search()}"
              class="InputField"
              :select-first-on-enter="true">
          </gmap-autocomplete>
      </v-col>

    </v-row>
  </v-col>
</template>

<script>
export default {
  name: "Auto-Input",
  props: {
    incidences: Array,
  },
  data: () => ({
    startCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
    },
    endCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
  },
    stoptCity: {
      name: "",
      canton: "",
      incident :null,
      address: "",
    },
  }),
  methods: {
    /*
      * emits startCity, endCity, stopCity
    */
    search() {
      this.$emit('search',this.startCity,this.endCity, this.stoptCity);
    },
    /*
      * emits if easterEgg is triggered
    */
    triggerEasterEgg(value){
      this.$emit('triggerEasterEgg',value);
    },
    /*
      * sets startCity
    */
    setStart(place){
      if(place.name === ""){
        this.startCity = {
          name: "",
          canton: "",
          incident :null,
          address: "",
        }
        return;
      }
      this.startCity.address = place.formatted_address;
      //get Cityname an Canton
      place.address_components.forEach(x => {
            if (x.types.includes("locality")) {
              this.startCity.name = this.correctCityName(x);
            } else if (x.types.includes("administrative_area_level_1")) {
              this.startCity.canton = x.short_name;
            }
          }
      )
      //search for City in our database and fils array with cityname and the corrisponding incident
      const city = this.incidences.find(v => v.name === this.startCity.name && v.canton === this.startCity.canton);
      if (city != undefined) {
        this.startCity.incident = Math.round(city.incident);
      } else {
        this.startCity.incident = "Keine Daten verfügbar";
        //logs all city which weren't found in our database
      }
    },
    /*
      * sets stopCity
    */
    setPause(place){
      if(place.name === "" ){
        this.stoptCity = {
              name: "",
              canton: "",
              incident :null,
              address: "",
        }
        return;
      }
      this.stoptCity.address = place.formatted_address;
      place.address_components.forEach(x => {
            if (x.types.includes("locality")) {
              this.stoptCity.name = this.correctCityName(x);
            } else if (x.types.includes("administrative_area_level_1")) {
              this.stoptCity.canton = x.short_name;
            }
          }
      )
      //search for City in our database and fils array with cityname and the corrisponding incident
      const city = this.incidences.find(v => v.name === this.stoptCity.name && v.canton === this.stoptCity.canton);
      if (city != undefined) {
        this.stoptCity.incident = Math.round(city.incident);
      } else {
        this.stoptCity.incident = "Keine Daten verfügbar";
        //logs all city which weren't found in our database
      }
    },
    /*
      * sets endCity
    */
    setEnd(place){
      if(place.name === "" ){
        this.endCity = {
          name: "",
          canton: "",
          incident :null,
          address: "",
        }
        return;
      }
      this.endCity.address = place.formatted_address;
      if(this.endCity.address === "Bahnhofstrasse 6, 5210 Windisch, Schweiz"){
        this.triggerEasterEgg(true);
      }else {
        this.triggerEasterEgg(false);
      }

      place.address_components.forEach(x => {
            if (x.types.includes("locality")) {
              this.endCity.name = this.correctCityName(x);
            } else if (x.types.includes("administrative_area_level_1")) {
              this.endCity.canton = x.short_name;
            }
          }
      )
      //search for City in our database and fils array with cityname and the corrisponding incident
      const city = this.incidences.find(v => v.name === this.endCity.name && v.canton === this.endCity.canton);
      if (city != undefined) {
        this.endCity.incident = Math.round(city.incident);
      } else {
        this.endCity.incident = "Keine Daten verfügbar";
        //logs all city which weren't found in our database
      }
    },
    /*
      * corrects some wrong values given by google api
    */
    correctCityName(city){
      if (city.long_name.includes("Sankt")) {
        return city.long_name.replace("Sankt", "St.")
      }else if(city.long_name.includes("Biel")){
        return city.long_name.concat("/Bienne")
      }else if(city.long_name.includes("Kanton Reinach")){
        return city.long_name.replace("Kanton ", "")
      } else {return city.long_name;}
    },
  }
}
</script>

<style scoped>
.InputField{
  width: 100%;
  height: 4vh;
  box-shadow: 0px 3px 1px -2px rgb(0 0 0 / 20%),
  0px 2px 2px 0px rgb(0 0 0 / 14%),
  0px 1px 5px 0px rgb(0 0 0 / 12%);

  padding: 0 12px;
  font-size: 16px;
  border-radius: 6px;

}
</style>
