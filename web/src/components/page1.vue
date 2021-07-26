<template>
  <div>
    <video-background
      src="http://131.mollnn.com:5002/travel_cloud.mp4"
      style="max-height: 100vh; height: 100vh "
    >
    </video-background>
    <Page1background />
    <checkbox1 class="box1" />
    <checkbox2 class="box2" />
    <el-button type="primary" round @click="gotolink" class="btn"
      >Let's go!</el-button
    >
  </div>
</template>

<script>
import checkbox1 from "./checkbox1.vue";
import checkbox2 from "./checkbox2.vue";

import Bus from "../bus1.js";
export default {
  data() {
    return {
      value: [],
    };
  },
  methods: {
    gotolink() {
      this.$router.push("/page2");
      this.value[0] = this.$children[1].value;
      this.value[1] = this.$children[2].value;
      var tmp = this.value;

      setTimeout(function () {
        Bus.$emit("change", tmp);
        console.log(tmp);
      }, 1000);
    },
  },
  components: {
    checkbox1,
    checkbox2,
  },
};
</script>

<style scoped>
.btn {
  position: absolute;
  text-align: center;
  top: 70vh;
  left: 600px;
  padding: 10px;
}
.box1 {
  text-align: center;
  position: absolute;
  top: 30vh;
  left: 40%;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}
.box2 {
  text-align: center;
  position: absolute;
  top: 50vh;
  left: 40%;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}
</style>
