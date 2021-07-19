<template>
  <div class="xx" style="height:100%">
<el-container id="hh" style="height:100%">
  <el-header style="height:5%">
    <Page3header/>
  </el-header>
  <el-container  style="height:70%">
      <el-main>
        <Page3videoplayer/>
      </el-main>
    <el-aside width="40%">
      <Page3rightzone/>
    </el-aside>
  </el-container>
      <div>
        <Page3bottom/>
      </div>
</el-container>
  </div>
</template>
<script>
import Page3header from './Page3header.vue'
import Page3videoplayer from './Page3videoplayer.vue'
import Page3rightzone from './Page3rightzone.vue'
import Page3bottom from './Page3bottom.vue'
export default {
  name: "HelloWorld",
  components:{
    Page3header,
    Page3videoplayer,
    Page3rightzone,
    Page3bottom
  }
};

</script>
<style>
  .el-header{
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }

  html,body,#app,.xx,.el-container {
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

</style>