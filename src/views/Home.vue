<template>
  <div class="home">
    <v-container>
      <v-layout>
        <v-row align-content="center">
          <v-col align="center">
            <h2>Welcome</h2>
            <v-btn x-large color="primary" href="http://localhost:8080/login">Login</v-btn>
          </v-col>
        </v-row>
      </v-layout>
    </v-container>


  </div>
</template>

<script>
// @ is an alias to /src

//import Login from '@/components/Login'
export default {
  name: 'Home',
  components: {
    //Login

  }
}
</script>
