import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#c44348',
                zugMain: '#2B42BF',
                zugAcent: '#021749',
                autoMain: '#c44348',
                statusMain: '#43a047'
            },
        },
    },
})



