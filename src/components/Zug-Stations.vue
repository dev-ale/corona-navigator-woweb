<template>
  <div>
    <v-row>
      <v-col>
        <div class="anzeigetafel" >
          <v-row>
            <v-col>
              <h3>{{departure.time}}</h3>
            </v-col>
            <v-col></v-col>
            <v-col></v-col>
            <v-col align="right">
              <v-chip small dark label color="red">{{ departure.type }}</v-chip>
            </v-col>
          </v-row>
          <v-row>
            <h1>{{departure.name}}</h1>
          </v-row>
        </div>
      </v-col>
      <v-col>
        <div class="anzeigetafel">
          <v-row>
            <v-col>
              <h3>{{arrival.time}}</h3>
            </v-col>
            <v-col></v-col>
            <v-col></v-col>
            <v-col align="right">
              <v-chip small dark label color="red">{{ arrival.type }}</v-chip>
            </v-col>
          </v-row>
          <v-row>
            <h1 class="mr-5">{{arrival.name}}</h1>
          </v-row>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div class="anzeigetafel">
          <v-list color="transparent" dense >
            <v-list-item class="white--text">
              <v-list-item-avatar class="white--text">Nr</v-list-item-avatar>
              <v-list-item-title class="white--text">Stationen</v-list-item-title>
              <v-list-item-subtitle class="white--text">14 Tage Inzidenz</v-list-item-subtitle>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item v-for="(station, index) of stations" :key="station.name" class="white--text">
              <v-list-item-avatar color="white">
                {{ index + 1}}
              </v-list-item-avatar>
              <v-list-item-title class="white--text">
                <h2>{{ station.name }}</h2>
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip label v-if="!isNaN(station.incident)"color="red" dark>{{ Math.round(station.incident) }}</v-chip>
                <v-chip label small v-if="isNaN(station.incident)" color="red" dark>{{ station.incident }}</v-chip>
              </v-list-item-subtitle>
              <v-divider
                  v-if="index"
                  :key="index"
              ></v-divider>
            </v-list-item>

          </v-list>
        </div>
      </v-col>
    </v-row>
  </div>

</template>

<script>
export default {
  name: "Zug-Stations",
  props: {
    stations: Array,
    arrival: Object,
    departure: Object
  },
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
