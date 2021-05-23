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
        failure () {
            this.$emit('failure')
        },
    },

    props: {
        origin: { type: Object },
        destination: { type: Object },
        location: {type: Object},
        travelMode: { type: String },
        search: {type: Function},
        count: {type: Number}
    },

    afterCreate(directionsRenderer) {
        let directionsService = new window.google.maps.DirectionsService();
        this.$watch(
            () => [this.origin, this.destination, this.travelMode, this.location],
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
                        if (status !== "OK") {
                            this.failure();
                        }else {
                            directionsRenderer.setDirections(response);
                            this.getDirections(response)
                        }
                    }
                );
            }
        );
    }
});
