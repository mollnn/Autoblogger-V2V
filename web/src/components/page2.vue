<template>
  <div>
    <transition name="fade">
      <Loading v-if="isLoading"></Loading>
    </transition>
    <el-row
      ><el-button type="primary" class="button" @click="goback"
        >返回</el-button
      ></el-row
    >
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
          :body-style="{ padding: '15px' }"
          shadow="hover"
          @click.native="gotolink(index)"
        >
          <img :src="o" class="image" />
        </el-card>
      </el-col>
      <br />
    </el-row>
  </div>
</template>
<script>
import Bus from "../bus1.js";
import Loading from "@/components/loading";
var tempuse = [1, 1];
export default {
  components: { Loading },
  data() {
    return {
      list: [],
      pplist: ["."],
      kklist: [],
      isLoading: true,
    };
  },
  methods: {
    gotolink: function (index) {
      this.$store.state.index = index;
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
          this.list = res.data;
          this.$store.state.objlist = res.data;
          for (var i = 0; i < res.data.length; ++i) {
            this.pplist[i] =
              "http://131.mollnn.com:5001/poster/" + res.data[i].id + "/";
            this.kklist[i] =
              "http://131.mollnn.com:5001/video/" + res.data[i].id + "/";
          }
          this.$store.state.posterlist = this.pplist;
          this.$store.state.videolist = this.kklist;
          console.log(this.$store.state.posterlist);
          document.getElementById("elcol").value = this.pplist;
          this.$forceUpdate();
          this.isLoading = false;
        });
    },
  },

  mounted() {
    // this.draw();
    Bus.$on("change", (val) => {
      tempuse = val;
      console.log("fuck me");
      // setTimeout(function () {
      //   this.isLoading = false;
      //   this.$forceUpdate();
      // }, 2000);
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
</style>
