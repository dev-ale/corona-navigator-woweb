<template>
  <v-col align="center">
    <v-row>
      <v-col sm="4" xs="4" md="4" cols="12">
        <v-text-field solo clearable v-model="from" placeholder="von"></v-text-field>
      </v-col>
      <v-col sm="4" xs="4" md="4" cols="12">
        <v-text-field v-on:keyup.enter="search" solo clearable v-model="to" placeholder="bis"></v-text-field>
      </v-col>
      <v-col sm="4" xs="4" md="4" cols="12" align="left">
        <v-btn @click="search" width="100%" color="primary" dark x-large>Suchen</v-btn>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
export default {
  name: "Zug-Input",

  data: () => ({
    from: "",
    to: "",

  }),
  methods: {
    search() {
      this.$emit('search',this.from,this.to);
    }
  }
}
</script>

<style scoped>

</style>
