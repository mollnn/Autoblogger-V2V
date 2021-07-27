<template>
<div>
    <div class="bg" />

  <transition name="fade" mode="in-out">
    <router-view></router-view>
  </transition>

  </div>
</template>

<script>


export default {
  name: "App",
  data() {
    return {
      transitionName: "",
    };
  },
  created() {
    const currentPath = this.$router.history.current.path;
    if (
      window.localStorage.getItem("authenticated") === "false" ||
      currentPath === "/" ||
      currentPath === "/app"
    ) {
      this.$router.push("/page1");
    }
  },
};
</script>

<style>
.fade-enter {
 
 opacity:0;
 
}
 
.fade-leave{
 
 opacity:1;
 
}
 
.fade-enter-active{
 
 transition:opacity .8s;
 
}
 
.fade-leave-active{
 
 opacity:0;
 
 transition:opacity .3s;
 
}
</style>


<style>
	.bg{
    width: 100%;

    height: 100%;

    background-color: #000;

    position: fixed;
    z-index: -999;
  }
</style>