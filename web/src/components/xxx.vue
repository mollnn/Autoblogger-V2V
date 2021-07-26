<template>
  <div>
    <div>{{pplist}}</div>
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
          @click.native="gotolink"
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
var tempuse = [0,0];
export default {
  data() {
    return {
      list: [],
      pplist: [2],
    };
  },
  methods: {
    gotolink: function () {
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
          for (var i = 0; i < res.data.length; ++i) {
            console.log(i);
            this.pplist[i] =
              "http://131.mollnn.com:5001/poster/" + res.data[i].id + "/";
          }
          console.log("hahaha");
          console.log(this.pplist);
          this.$forceUpdate();
          // this.$set(this.pplist,0,this.pplist);
        });
    },
  },

  mounted() {
    Bus.$on("change", (val) => {
      tempuse = val;
      console.log("hhh");
      console.log(val);
      this.draw();
    });

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
