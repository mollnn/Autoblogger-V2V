<template>
  <div>
    <h2 id="descs" class="text-muted mb-0 mr" style="font-size: 13px">
      <small>...</small>
    </h2>
  </div>
</template>

<script>
var tempuse = "BV1144y1q7ve";
import Bus from ".././bus.js";
export default {
  name: "vinfodescslabel",
  data() {
    return {};
  },
  methods: {
    ttt() {
      var elem1 = document.getElementById("descs");
      elem1.textContent = "...";
      this.draw();
    },
    draw() {
      var elem1 = document.getElementById("descs");
      this.$http
        .get("http://131.mollnn.com:5000/api/v/info/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          elem1.textContent = res.data[0].descs;
        });
    },
  },
  mounted() {
    Bus.$on("change", (val) => {
      tempuse = val;
      this.ttt();
    });
    this.draw();
  },
};
</script>

<style></style>