<template>
  <div id="app">
    <GoogleMap />
  </div>
</template>

<script>
import * as VueGoogleMaps from "vue2-google-maps";
import GoogleMap from "./components/map.vue";

export default {
  name: "app",
  components: {
    GoogleMap
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

