<template>
  <div class="header">
    <el-page-header
      id="xxx3"
      content="播放页"
      style="color: #fff; line-height: 40px !important"
    >
    </el-page-header>
    <el-tooltip
      effect="dark"
      :content="video_info"
      class="item"
      placement="bottom-end"
      id="xxx4"
    >
      <el-button
        type="primary"
        round
        style="
          float: right !important;
          position: absolute !important;
          top: 0px !important;
          right: 100px !important;
          background-color: #f2b632 !important;
          color: #fff !important;
          border: 0px !important;
        "
        >视频信息</el-button
      >
    </el-tooltip>
    <el-button
      type="primary"
      round
      @click.native="gobackhhh"
      style="
        float: right;
        position: absolute;
        top: 0px;
        right: 0px;
        background-color: #444;
        border: 0px;
      "
      >返回</el-button
    >
  </div>
</template>
<script>
import Bus from "../bus1.js";
var tempuse = "";
export default {
  data() {
    return { video_info: "video info" };
  },
  methods: {
    draw() {
      tempuse = this.$store.state.objlist[
        this.$store.state.objlist.length - 1 - this.$store.state.index
      ].id;
      this.$http
        .get("http://v2v.mollnn.com:5000/vinfo/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          document.getElementById("xxx3").textContent = res.data[0].title;
          this.video_info = "[" + res.data[0].bvid + "]  视频介绍：" + res.data[0].descs;
          this.$forceUpdate();
        });
    },
    gobackhhh() {
      // this.$store.state.isloading = false;
      this.$router.push("/page1");
      Bus.$emit("changebacktoPage2", this.$store.state.index);
    },
  },
  mounted() {
    console.log("headtookkk!");
    this.draw();
    Bus.$on("changethebottom", (val) => {
      console.log(val);
      this.draw();
    });
    Bus.$on("changevideo", (val) => {
      console.log(val);
      this.draw();
    });
  },
};
</script>
