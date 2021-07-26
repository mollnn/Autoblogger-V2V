<template>
  <el-card class="box-card">
    <div id= "xxxx1">Loading....</div><br>
    <div id= "xxxx2">Loading....</div><br>
    <div id= "xxxx3">Loading....</div><br>
    <div id= "xxxx4">Loading....</div><br>
  </el-card>
</template>

<script>
var tempuse = '';
import Bus from "../bus1.js";
export default {
  data() {
    return {
    };
  },
  methods: {
        draw() {
          tempuse = this.$store.state.objlist[this.$store.state.index].id;
      this.$http
        .get(
          "http://131.mollnn.com:5001/xv/danmu/" +
            tempuse+
            "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          console.log(res);
          document.getElementById("xxxx1").textContent = res.data[0][0];
          document.getElementById("xxxx2").textContent = res.data[1][0];
          document.getElementById("xxxx3").textContent = res.data[2][0];
          document.getElementById("xxxx4").textContent = res.data[3][0];
        });
    },
  },
  mounted() {
     console.log("rightookkk!");
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
</script>>


<style>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 0px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 100%;
  height: 40%;
  background-color: #282828;
}
</style>