import { MapElementFactory } from "vue2-google-maps";

export default MapElementFactory({
    name: "directionsRenderer",
    response: 'empty',
    ctr() {
        return window.google.maps.DirectionsRenderer;
    },

    events: [],

    mappedProps: {},

    methods: {
        getDirections (res) {
            this.$emit('getDirections', res)
        },
    },

    props: {
        origin: { type: String },
        destination: { type: String },
        location: {type: String},
        travelMode: { type: String },
        search: {type: Function},
        count: {type: Number}
    },

    afterCreate(directionsRenderer) {
        let directionsService = new window.google.maps.DirectionsService();
        this.$watch(
            () => [this.count],
            () => {
                let { origin, destination, travelMode, location } = this;
                if (!origin || !destination || !travelMode) return;

                let request;
                if(location){
                    request = {
                        origin,
                        destination,
                        waypoints: [
                            {
                                location: location,
                                stopover: true,
                            }
                        ],
                        travelMode
                    }
                }else {
                    request = {
                        origin,
                        destination,
                        travelMode
                    }
                }

                directionsService.route(
                    request,
                    (response, status) => {
                        if (status !== "OK") return;
                        directionsRenderer.setDirections(response);
                        this.getDirections(response)
                        //console.log(response.routes[0].legs[0].duration)
                    }
                );
            }
        );
    }
});
