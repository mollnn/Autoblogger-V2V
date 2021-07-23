<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-lg">
      <h2 id="sview">...</h2>
      <i class="la la-arrow-right text-primary la-lg rotate-315" />
    </div>
    <div class="d-flex flex-wrap justify-content-between">
      <div class="mt">
        <h6 id="scnt">...</h6>
        <p class="text-muted mb-0 mr"><small>视频总数</small></p>
      </div>
      <div class="mt">
        <h6 id="sdanmuku">...</h6>
        <p class="text-muted mb-0"><small>总弹幕数</small></p>
      </div>
      <div class="mt">
        <h6 id="slikes">...</h6>
        <p class="text-muted mb-0 mr"><small>总点赞数</small></p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "sumlabel",
  data() {
    return {};
  },
  methods: {
    draw() {
      var elemsview = document.getElementById("sview");
      var elemscnt = document.getElementById("scnt");
      var elemsdanmuku = document.getElementById("sdanmuku");
      var elemslikes = document.getElementById("slikes");
      this.$http
        .get("http://131.mollnn.com:5000/api/sum/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          elemsview.textContent = res.data[0].sview;
          elemscnt.textContent = res.data[0].scnt;
          elemsdanmuku.textContent = res.data[0].sdanmaku;
          elemslikes.textContent = res.data[0].slikes;
        });
    },
  },
  mounted() {
    this.draw();
  },
};
</script>

<style></style>