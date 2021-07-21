
<template>
  <div>
    <el-container class="black">
      <el-header>
        <checkbox3 class="box3" />
        <checkbox4 class="box4" />
        <el-button type="primary" round @click="getagain" class="btn"
          >Let's go!</el-button
        >
      </el-header>
      <transition name="fade">
        <Loading v-if="isLoading">
        </Loading>
      </transition>
      <el-row><div style="padding: 10px"></div></el-row>
      <el-row>
        <el-col
          id="elcol"
          :span="4"
          v-for="(o, index) in pplist"
          :value="pplist"
          :key="o"
          :offset="index % 4 == 0 ? 2 : 1"
        >
          <el-card
            :body-style="tstyle"
            shadow="hover"
            @click.native="gotolink(index)"
          >
            <img :src="o" class="image" />
          </el-card>
          <div style="padding: 10px"></div>
        </el-col>

        <br />
      </el-row>
    </el-container>
  </div>
</template>
<script>
import Bus from "../bus1.js";
import Loading from "@/components/loading";
import checkbox3 from "./checkbox3.vue";
import checkbox4 from "./checkbox4.vue";
var tempuse = [1, 1];
export default {
  components: { 
    Loading,
   checkbox3, checkbox4 },
  data() {
    return {
      tstyle: { "background-color": "#111", padding: "8px" },
      list: [],
      pplist: ["."],
      kklist: [],
      isLoading: true,
      val: [],
    };
  },
  methods: {
    getagain: function () {
      console.log(this.$children[0].$children[0].$children[0].value);
      this.val[0] = this.$children[0].$children[0].$children[0].value;
      this.val[1] = this.$children[0].$children[0].$children[1].value;
      tempuse = this.val;
      console.log(tempuse);
      this.$forceUpdate();
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
        .get(
          "http://131.mollnn.com:5001/list/" +
            tempuse[0] +
            "/" +
            tempuse[1] +
            "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          var len = res.data.length;
          if (len >= 100) len = 100;
          this.list = res.data.slice(0, len);
          this.$store.state.objlist = res.data.slice(0, len);
          for (var i = 0; i < len; ++i) {
            this.pplist[i] =
              "http://131.mollnn.com:5001/poster/" + res.data[i].id + "/";
            this.kklist[i] =
              "http://131.mollnn.com:5001/video/" + res.data[i].id + "/";
          }
          this.$children[0].$children[0].$children[0].value = tempuse[0];
          this.$store.state.value3 = this.$children[0].$children[0].$children[0].value;
          this.$children[0].$children[0].$children[1].value = tempuse[1];
          this.$store.state.value4 = this.$children[0].$children[0].$children[1].value;
          this.$store.state.posterlist = this.pplist;
          this.$store.state.videolist = this.kklist;
          console.log(this.$store.state.posterlist);
          document.getElementById("elcol").value = this.pplist;
          this.isLoading = false;
          this.$forceUpdate();
          console.log("aaaaaaaaaaaaaaaaaa");
          console.log(this.isLoading);
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
  float: right;
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
</style>
