<template>
  <div class="xx" style="height: 100%" :style="styles">
    <el-container id="hh" style="height: 100%">
      <el-header style="height: 7%">
        <Page3header />
      </el-header>
      <el-container style="height: 65%">
        <el-main>
          <Page3videoplayer />
        </el-main>
        <el-aside width="35%">
          <Page3rightzone />
          <dammuciyun />
        </el-aside>
      </el-container>
      <el-footer>
        <div>
          <Page3bottom />
        </div>
      </el-footer>
    </el-container>
  </div>
</template>
<script>
import Page3header from "./Page3header.vue";
import Page3videoplayer from "./Page3videoplayer.vue";
import Page3rightzone from "./Page3rightzone.vue";
import Page3bottom from "./Page3bottom.vue";
import dammuciyun from "./danmuciyun.vue";
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
    Page3rightzone,
    Page3bottom,
    dammuciyun,
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
  line-height: 60px;
  height: 20% !important;
}

.el-aside {
  background-color: #282828;
  color: #333;
  text-align: center;
  line-height: 18px;
}

.el-main {
  background-color: #222;
  color: #333;
  text-align: center;
  line-height: 160px;
  height: calc(100vh - 100px);
}

body > .el-container {
  margin-bottom: 40px;
}

html,
body,
#app,
.xx,
.el-container {
  padding: 0px;
  margin: 0px;
  height: 100%;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
.text {
  font-size: 14px;
  color:white !important
}

.item {
  padding: 18px 0;
}

.box-card {
  background-color:#222 !important;
  width: 100%;
  height: 38%;
  background-color: #282828;
  color:white !important
}


</style>