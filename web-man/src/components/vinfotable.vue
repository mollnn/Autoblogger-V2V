<template>
  <div class="table-responsive">
    <table class="table table-striped table-lg mb-0 requests-table">
      <thead>
        <tr class="text-muted">
          <th>视频id</th>
          <th>up id</th>
          <th>是否转载</th>
          <th>分区</th>
          <th>播放</th>
          <th>投币</th>
          <th>评论</th>
          <th>点赞</th>
          <th>收藏</th>
        </tr>
      </thead>
      <tbody>
        <td id="bvid"></td>
        <td id="aid"></td>
        <td id="iscopy"></td>
        <td id="tname"></td>
        <td id="view"></td>
        <td id="coin"></td>
        <td id="reply"></td>
        <td id="likes"></td>
        <td id="favorite"></td>
      </tbody>
    </table>
  </div>
</template>

<script>
var tempuse = "BV1144y1q7ve";
import Bus from ".././bus.js";
export default {
  name: "vinfotable",
  data() {
    return {};
  },
  methods: {
    ttt() {
      var elem1 = document.getElementById("bvid");
      var elem2 = document.getElementById("aid");
      var elem3 = document.getElementById("iscopy");
      var elem4 = document.getElementById("tname");
      var elem5 = document.getElementById("view");
      var elem6 = document.getElementById("coin");
      var elem7 = document.getElementById("reply");
      var elem8 = document.getElementById("likes");
      var elem9 = document.getElementById("favorite");
      elem1.textContent = "...";
      elem2.textContent = "...";
      elem3.textContent = "...";
      elem4.textContent = "...";
      elem5.textContent = "...";
      elem6.textContent = "...";
      elem7.textContent = "...";
      elem8.textContent = "...";
      elem9.textContent = "...";
      this.draw();
    },
    draw() {
      var elem1 = document.getElementById("bvid");
      var elem2 = document.getElementById("aid");
      var elem3 = document.getElementById("iscopy");
      var elem4 = document.getElementById("tname");
      var elem5 = document.getElementById("view");
      var elem6 = document.getElementById("coin");
      var elem7 = document.getElementById("reply");
      var elem8 = document.getElementById("likes");
      var elem9 = document.getElementById("favorite");
      this.$http
        .get("http://131.mollnn.com:5000/api/v/info/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          elem1.textContent = res.data[0].bvid;
          elem2.textContent = res.data[0].aid;
          if (res.data[0].iscopy) elem3.textContent = "是";
          else elem3.textContent = "否";
          elem4.textContent = res.data[0].tname;
          elem5.textContent = res.data[0].view;
          elem6.textContent = res.data[0].coin;
          elem7.textContent = res.data[0].reply;
          elem8.textContent = res.data[0].likes;
          elem9.textContent = res.data[0].favorite;
        });
    },
  },
  mounted() {
    Bus.$on("change", (val) => {
      tempuse = val;
      this.ttt();
      // alert(tempuse);
    });
    this.draw();
  },
};
</script>

<style></style>