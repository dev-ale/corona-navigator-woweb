<template>
  <v-container>
    <h2>Auto</h2>
    <GmapMap
        :center="entryPoint"
        :zoom="10"
        style="width: 1150px; height: 600px"
    >
      <GmapMarker
          v-for="(m, index) in markers"
          :key="index"
          :position="m.position"
      />
    </GmapMap>
  </v-container>

</template>

<script>
export default {
  name: "Auto",
  data: () => ({
    markers: [
        {
          name: 'start',
          position: {
            lat:47.559601,
            lng:7.588576
          }
        },
        {
          name: 'end',
          position: {
            lat:47.4722,
            lng:7.6194
          }
        },
      {
        name: 'pause',
        position: {
          lat:47.5167,
          lng:7.6167
        }
      }
    ],

    entryPoint: {
      lat:47.4722,
      lng:7.6194
    }
  }),

}
</script>

<style scoped>

</style>
