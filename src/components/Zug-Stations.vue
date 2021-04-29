<template>
  <v-row>
    <v-col cols="4">
      <v-list dense v-for="station of stations" :key="station.name">
        <v-list-item>
          <v-list-item-title>
            <h2>{{ station.name }}</h2>
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-chip v-if="!isNaN(station.incident)"color="primary" dark>{{ Math.round(station.incident) }}</v-chip>
            <v-chip v-if="isNaN(station.incident)" outlined color="primary" dark>{{ station.incident }}</v-chip>
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Zug-Stations",
  props: {
    stations: Array,
  },
}
</script>

<style scoped>

</style>
