<template>
  <div>
    <el-container class="black">
      <el-header>
        <checkbox3 class="box3" />
        <el-button type="primary" round @click="getagain" class="btn"
          >Let's go!</el-button
        >
      </el-header>
      <el-row><div style="padding: 10px"></div></el-row>
      <el-row v-show="count_img_load >= 30">
        <el-col
          id="elcol"
          class="elcol"
          :span="4"
          v-for="(o, index) in pplist"
          :value="pplist"
          :key="o"
          :offset="index % 4 == 0 ? 2 : 1"
        >
          <el-card :body-style="tstyle" shadow="hover" @click.native="gotolink(index)">
            <img :src="o" @load="handleLoad" class="image" />
          </el-card>
          <div style="padding: 10px"></div>
        </el-col>

        <br />
      </el-row>
      <el-row v-show="count_img_load < 30"> <img src="http://39.101.139.97:8000/imgs/page2-loading.png" class="loadingimg"> </el-row>
    </el-container>
  </div>
</template>
<script>
import Bus from "../bus1.js";
import checkbox3 from "./checkbox3.vue";
var tempuse = [1, 1];
export default {
  components: {
    checkbox3,
  },
  data() {
    return {
      tstyle: { "background-color": "#111", padding: "8px" },
      list: [],
      pplist: [
        "http://39.101.139.97:8000/imgs/loading.png",
        "http://39.101.139.97:8000/imgs/loading.png",
        "http://39.101.139.97:8000/imgs/loading.png",
        "http://39.101.139.97:8000/imgs/loading.png",
      ],
      kklist: [],
      isLoading: true,
      val: [],
      count_img_load: 0,
    };
  },
  methods: {
    handleLoad() {
      this.count_img_load++;
      console.log(this.count_img_load);
      if(this.count_img_load>=50){
        this.isLoading=false;
      }
    },
    getagain: function () {
      console.log(this.$children[0].$children[0].$children[0].value);
      this.val[0] = this.$children[0].$children[0].$children[0].value;
      this.val[1] = this.$children[0].$children[0].$children[1].value;
      tempuse = this.val;
      console.log(tempuse);
      this.isLoading = true;
      this.draw();
    },
    gotolink: function (index) {
      console.log("???");
      this.$store.state.index = this.$store.state.videolist.length - 1 - index;
      this.$store.state.vlink = this.kklist[index];
      this.$router.push("/page3");
    },
    goback: function () {
      this.$router.push("/page1");
    },
    draw() {
      this.$http
        .get("http://39.101.139.97:5000/list/" + tempuse[0] + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.pplist = [
            "http://39.101.139.97:8000/imgs/loading.png",
            "http://39.101.139.97:8000/imgs/loading.png",
            "http://39.101.139.97:8000/imgs/loading.png",
            "http://39.101.139.97:8000/imgs/loading.png",
          ];
          this.$forceUpdate();
          this.isLoading=true;
          this.count_img_load = 0;
          var len = res.data.length;
          if (len >= 100) len = 100;
          this.list = res.data.slice(0, len);
          this.$store.state.objlist = res.data.slice(0, len);
          this.$children[0].$children[0].$children[0].value = tempuse[0];
          this.$store.state.value3 = this.$children[0].$children[0].$children[0].value;
          this.$children[0].$children[0].$children[1].value = tempuse[1];
          this.$store.state.value4 = this.$children[0].$children[0].$children[1].value;
          for (var i = 0; i < len; ++i) {
            this.pplist[i] =
              "http://39.101.139.97:5000/poster/" +
              this.$store.state.objlist[i].id +
              "/";
            this.kklist[i] =
              "http://39.101.139.97:8081/output/" + this.$store.state.objlist[i].id + ".mp4";
          }
          document.getElementById("elcol").value = this.pplist;
          this.isLoading = false;
          this.$forceUpdate();
          this.$store.state.posterlist = this.pplist;
          this.$store.state.videolist = this.kklist;
        });
    },
  },

  mounted() {
    // this.draw();
    // if(this.$store.state.isloading == false){
    //   this.isLoading = false;
    // }
    Bus.$on("change", (val) => {
      tempuse = val;
      console.log("fuck me");
      // setTimeout(function () {
      //   this.isLoading = false;
      //   this.$forceUpdate();
      // }, 2000);
      this.draw();
    });
    Bus.$on("changebacktoPage2", (val) => {
      this.isLoading = false;
      console.log(val);
      tempuse[0] = this.$store.state.value3;
      tempuse[1] = this.$store.state.value4;
      this.draw();
    });
    // setTimeout(function () {
    //   this.isLoading = false;
    //   this.$forceUpdate();
    // }, 2000);
  },
};
</script>
<style>
.box3 {
  right: 5%;
}
.box4 {
  left: 10%;
}
.btn {
}
.black {
  background-color: #222;
}
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  height: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
  height: 20vh;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
  height: 80vh;
}

.el-card {
  border: 0px #222 !important;
  width: 100% !important;
  height: 100% !important;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.loadingimg {
  width: 100% !important;
  height: 100% !important;
}
</style>
