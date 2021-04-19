<template>
  <v-app>
    <v-app-bar
        app
        color="primary"
        dark
    >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-spacer></v-spacer>

      <div class="d-flex align-center">
        <h2>Corona-Navigator</h2>
      </div>

      <v-spacer></v-spacer>

      <v-btn
          href="https://gitlab.fhnw.ch/wodss-wowm-group-bs-bl/webservice-bl-bs"
          target="_blank"
          text
      >
        <span class="mr-2">GitLab</span>
        <v-icon>mdi-gitlab</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col align=" center" cols="6">
            <v-card
                max-width="475"
                class="mx-auto"
            >
              <v-toolbar
                  color="teal"
                  dark
              >
                <v-spacer></v-spacer>
                <v-toolbar-title>sampledata</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-list dense v-for="incidence of incidences">
                <v-list-item>
                  <v-list-item-title>
                    <h2>{{ incidence.name }}</h2>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip color="teal" dark>{{ incidence.incident }}</v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>

      </v-container>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  data: () => ({
    incidences: [{
      timeStamp: "timestamp",
      name: "Basel",
      canton: "BS",
      date: "2021-04-19",
      incident: "272",
    },
      {
        timeStamp: "timestamp",
        name: "Aesch",
        canton: "BL",
        date: "2021-04-19",
        incident: "201",
      }]
  }),
};
</script>
