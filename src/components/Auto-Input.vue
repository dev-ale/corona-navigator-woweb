<template>
  <v-col align="center">
    <v-row>
      <v-col sm="3" xs="3" md="3" cols="12">
        <v-text-field @keyup.enter="search" solo clearable v-model="start" placeholder="von"></v-text-field>
      </v-col>

      <v-col sm="3" xs="3" md="3" cols="12">
        <v-text-field @keyup.enter="search" solo clearable v-model="stoppoint" placeholder="pause"></v-text-field>
      </v-col>

      <v-col sm="3" xs="3" md="3" cols="12">
        <v-text-field @keyup.enter="search" solo clearable v-model="end" placeholder="bis"></v-text-field>
      </v-col>

      <v-col sm="3" xs="3" md="3" cols="12">
        <v-btn @click="search" width="100%" outlined color="primary" dark x-large>Suchen</v-btn>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
export default {
  name: "Auto-Input",
  data: () => ({
    start: "",
    end: "",
    stoppoint: "",
  }),
  methods: {
    search() {
      this.$emit('search',this.start,this.end, this.stoppoint);
    }
  }
}
</script>

<style scoped>

</style>
