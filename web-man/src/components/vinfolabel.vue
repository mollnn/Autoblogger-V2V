<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-lg">
      <h2 id="view">...</h2>
      <i class="la la-arrow-right text-primary la-lg rotate-315" />
    </div>
    <div class="d-flex flex-wrap justify-content-between">
      <div class="mt">
        <h6 id="likes">...</h6>
        <p class="text-muted mb-0 mr"><small>点赞量</small></p>
      </div>
      <div class="mt">
        <h6 id="danmaku">...</h6>
        <p class="text-muted mb-0"><small>弹幕量</small></p>
      </div>
      <div class="mt">
        <h6 id="duration">...</h6>
        <p class="text-muted mb-0 mr"><small>时长</small></p>
      </div>
    </div>
  </div>
</template>


<script>
var tempuse = "BV1144y1q7ve";
import Bus from ".././bus.js";
export default {
  name: "vinfolabel",
  data() {
    return {
      val: "",
    };
  },
  methods: {
    ttt() {
      var elemview = document.getElementById("view");
      var elemlikes = document.getElementById("likes");
      var elemdanmaku = document.getElementById("danmaku");
      var elemduration = document.getElementById("duration");
      elemview.textContent = "...";
      elemlikes.textContent = "...";
      elemdanmaku.textContent = "...";
      elemduration.textContent = "...";
      this.draw();
    },
    draw() {
      var elemview = document.getElementById("view");
      var elemlikes = document.getElementById("likes");
      var elemdanmaku = document.getElementById("danmaku");
      var elemduration = document.getElementById("duration");
      this.$http
        .get("http://131.mollnn.com:5000/api/v/info/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          elemview.textContent = res.data[0].view;
          elemlikes.textContent = res.data[0].likes;
          elemdanmaku.textContent = res.data[0].danmaku;
          elemduration.textContent = res.data[0].duration;
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