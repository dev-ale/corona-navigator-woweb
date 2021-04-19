<template>
  <v-row>
    <v-col cols="4">
      <v-list dense v-for="incidence of incidences" :key="incidence.name">
        <v-list-item>
          <v-list-item-title>
            <h2>{{ incidence.name }}</h2>
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-chip color="primary" dark>{{ incidence.incident }}</v-chip>
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-col>

  </v-row>

</template>

<script>
export default {
  name: "Zug",
  props: {
    incidences: Array,
  },

}
</script>

<style scoped>

</style>
