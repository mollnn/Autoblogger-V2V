<template>
  <div class="xx" style="height: 100%" :style="styles">
    <el-container id="hh" style="height: 100%">
      <el-header style="height: 10% !important">
        <Page3header />
      </el-header>
      <el-main>
        <Page3videoplayer
          style="
            width: 86% !important;
            left: 7% !important;
            position: absolute !important;
          "
        />
      </el-main>
      <el-footer>
          <Page3bottom />
      </el-footer>
    </el-container>
  </div>
</template>
<script>
import Page3header from "./Page3header.vue";
import Page3videoplayer from "./Page3videoplayer.vue";
import Page3bottom from "./Page3bottom.vue";
export default {
  name: "HelloWorld",
  data() {
    return {
      styles: {
        //  backgroundSize: cover;
      },
    };
  },
  components: {
    Page3header,
    Page3videoplayer,
    Page3bottom,
  },
};
</script>
<style>
.el-header {
  background-color: #333;
  color: red;
  text-align: center;
  line-height: 60px;
}

.el-footer {
  background-color: #333;
  color: #333;
  text-align: center;
  height: 130px !important;
}

.el-main {
  background-color: #222;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  margin-bottom: 10px;
}

html,
body,
#app,
.xx,
.el-container {
  padding: 0px;
  margin: 0px;
}

.text {
  font-size: 14px;
  color: white !important;
}

.item {
  padding: 18px 0;
}
</style>
