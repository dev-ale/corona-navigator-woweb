import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import './registerServiceWorker'
import vuetify from './plugins/vuetify';
import * as VueGoogleMaps from 'vue2-google-maps'
const dotenv = require('dotenv');

dotenv.config();

const moment = require('moment')
require('moment/locale/de-ch')

Vue.use(require('vue-moment'), {
  moment
})

Vue.use(VueGoogleMaps, {
  load: {
    key: process.env.VUE_APP_GOOGLEMAPS_API_KEY,
    libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)

    //// If you want to set the version, you can do so:
    // v: '3.26',
  },
});


Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
