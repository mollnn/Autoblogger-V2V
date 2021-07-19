<template>
  <div class="bottom">
    <div>{{this.$store.state.posterlist.length}}</div>
    <hooper itemsToShow="7"
    infiniteScroll="true"
    mouseDrag = "true"
    initialSlide = this.$store.state.index
    wheelControl = "true"
    hoverPause = "true"
    :v-for="(o,index) in this.$store.state.posterlist"
    >
      <slide> <img :src="o" > </slide>
    </hooper>
    <hooper-navigation slot="hooper-addons"></hooper-navigation>
  </div>
</template>


<script>
import {
  Hooper,
  Slide,
  Navigation as HooperNavigation
  } from 'hooper';
import "hooper/dist/hooper.css";

export default {
  name: "App",
  components: {
    Hooper,
    Slide,
    HooperNavigation
  },
  mounted() {
    
    this.$forceUpdate();
  },
};
</script>
<style>
  img{
    width:150px;
    height: 100px;
  }
</style>