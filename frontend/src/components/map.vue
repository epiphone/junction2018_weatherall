<template>
  <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
    <div id="header">
      <h2>Estimated city bike resupply demand in 2 hours</h2>
      <span>Based on <a href='https://en.ilmatieteenlaitos.fi/open-data'>past
          weather information</a>, <a href='https://www.teliacompany.com/en/about-the-company/internet-of-things/crowd-insights/'>Telia
          Crowd Insights data</a>
        &amp; <a href="https://digitransit.fi/en/developers/apis/1-routing-api/bicycling/">city
          bike statistics</a>.</span>
      <br />
      <br />
      <span>Check source at <a href='https://github.com/epiphone/junction2018-weatherall'>Github</a>.</span>
    </div>
    <gmap-map :center="center" :zoom="15" style="width: 100%; height: 100%;">
      <gmap-info-window :options="infoOptions" :position="infoWindowPos"
        :opened="infoWinOpen" @closeclick="infoWinOpen=false">
        {{infoContent}}
      </gmap-info-window>
      <gmap-marker :key="index" v-for="(m, index) in markers" :label="m.label"
        :position="m.position" :icon="m.icon" @click="onClick(m, index)"></gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
import { gmapApi } from "vue2-google-maps";

export default {
  name: "GoogleMap",
  data() {
    return {
      center: { lat: 60.1851, lng: 24.8325 },
      places: [],
      currentPlace: null,
      stations: [],
      infoContent: "",
      infoWindowPos: null,
      infoWinOpen: false,
      currentMidx: null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35
        }
      }
    };
  },
  mounted() {
    this.geolocate();
    this.getData();
  },
  computed: {
    google: gmapApi,
    markers: function() {
      const markers = this.stations.map(d => {
        let color = "green";
        if (d.predicted_bikes > 10) {
          color = "red";
        } else if (d.predicted_bikes > 8) {
          color = "orange";
        } else if (d.predicted_bikes > 0) {
          color = "yellow";
        }

        return {
          icon: {
            url: `http://maps.google.com/mapfiles/ms/icons/${color}.png`
          },
          label: `${d.name} (${d.predicted_bikes})`,
          infoText: `Bikes available: ${d.free_bikes} | Predicted demand: ${
            d.predicted_bikes
          } bike(s)`,
          position:
            this.google && new this.google.maps.LatLng(d.latitude, d.longitude)
        };
      });
      console.log("markers", JSON.parse(JSON.stringify(markers)));
      return markers;
    }
  },
  methods: {
    onClick: function(marker, index) {
      this.center = marker.position;
      this.toggleInfoWindow(marker, index);
      console.log("clicked", JSON.parse(JSON.stringify(marker)));
    },
    getData: function() {
      const headers = new Headers();
      let self = this;
      // const request = new Request("http://165.227.147.109/api/bikestations", {
      const request = new Request("http://localhost:5000/api/bikestations", {
        method: "GET",
        headers: headers,
        mode: "cors",
        cache: "default"
      });
      fetch(request)
        .then(function(response) {
          return response.json();
        })
        .then(function(response) {
          self.stations = response.stations;
          console.log(
            "fetched stations",
            JSON.parse(JSON.stringify(self.stations))
          );
        });
    },
    toggleInfoWindow: function(marker, idx) {
      this.infoWindowPos = marker.position;
      this.infoContent = marker.infoText;

      //check if its the same marker that was selected if yes toggle
      if (this.currentMidx == idx) {
        this.infoWinOpen = !this.infoWinOpen;
      }
      //if different marker set infowindow to open and reset current marker index
      else {
        this.infoWinOpen = true;
        this.currentMidx = idx;
      }
    },
    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  }
};
</script>

<style>
#header {
  position: absolute;
  top: 5px;
  right: 60px;
  width: 20%;
  min-width: 350px;
  z-index: 999;
  background-color: rgba(255, 255, 255, 0.8);
  /* padding-bottom: 5px; */
  text-align: left;
  padding: 0 5px 5px 10px;
  border: 1px solid gray;
}
</style>

