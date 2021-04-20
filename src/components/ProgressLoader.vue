<template>
  <v-row>
    <v-col cols="12" align="center">
      <v-progress-circular
          :size="100"
          color="primary"
          indeterminate
      ></v-progress-circular>
    </v-col>
  </v-row>

</template>

<script>
export default {
name: "ProgressLoader"
}
</script>

<style scoped>

</style>
