<template>
  <div>
    <transition name="fade" mode="in-out">
      <video-background
        src="http://v2v.mollnn.com:8000/video/background.mp4"
        style="max-height: 100vh; height: 100vh"
      >
      </video-background>
    </transition>
    <img :src="img_url" class="logo" />
    <checkbox1 class="box1" />
    <el-button type="primary" round @click="gotolink" class="btn">开始欣赏</el-button>
    <el-button type="primary" round @click="gotoback" class="btn2">管理后台</el-button>
  </div>
</template>

<script>
import checkbox1 from "./checkbox1.vue";

import Bus from "../bus1.js";
export default {
  data() {
    return {
      value: [],
      img_url: "http://39.101.139.97:8000/imgs/v2v-white-shadow.png",
      isLoading: false,
    };
  },
  methods: {
    gotolink() {
      this.$router.push("/page2");
      this.value[0] = this.$children[1].value;
      this.value[1] = this.$children[1].value;
      var tmp = this.value;

      setTimeout(function () {
        Bus.$emit("change", tmp);
        console.log(tmp);
      }, 300);
    },
    gotoback() {
      this.$router.push("/page1");
    },
  },
  components: {
    checkbox1,
  },
};
</script>

<style scoped>
.btn {
  position: absolute !important;
  text-align: center !important;
  top: 65vh;
  left: 46% !important;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  width: 8% !important;
}
.btn2 {
  position: absolute !important;
  text-align: center !important;
  top: 75vh;
  left: 45.4% !important;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  width: 8% !important;
}
.box1 {
  text-align: center;
  position: absolute;
  top: 50vh;
  width: 16% !important;
  left: 42%;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}
.logo {
  text-align: center;
  position: absolute;
  top: 15%;
  width: 20% !important;
  left: 40%;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}

.el-select .el-input.is-focus .el-input__inner {
  border-color: #e6a23c !important;
}

.el-select .el-input.is-focus .el-input__inner {
  border-color: #e6a23c;
}

.fade-enter {
  opacity: 0;
}

.fade-leave {
  opacity: 1;
}

.fade-enter-active {
  transition: opacity 0.5s;
}

.fade-leave-active {
  opacity: 0;

  transition: opacity 0.5s;
}
</style>
