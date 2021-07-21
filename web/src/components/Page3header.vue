<template>
  <div class="header">
    <el-page-header id = "xxx2"
      @back="goBack"
      content="V2V视频播放中..."
      style="color: #fff"
    >
    </el-page-header>
  </div>
</template>
<script>
import Bus from "../bus1.js";
var tempuse = "";
export default {
  methods: {
    draw() {
      tempuse = this.$store.state.objlist[this.$store.state.index].id;
      this.$http
        .get("http://131.mollnn.com:5001/vinfo/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          document.getElementById("xxx2").content = res.data[0].title;
        });
    },
    goBack() {
      this.$router.push("/page2");
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