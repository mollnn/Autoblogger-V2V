<template>
  <router-view></router-view>

</template>

<script>
export default {
  name: 'App',
  created() {
    const currentPath = this.$router.history.current.path;
    if (window.localStorage.getItem("authenticated") === "false"||currentPath === "/" || currentPath === "/app") {
      this.$router.push("/page1");
    }
  },
}
</script>

<style>

</style>
