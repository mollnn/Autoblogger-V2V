<template>
  <div>
    <Page3header/>
    <Page3videoplayer/>
    <Page3rightzone/>
    <Page3leftzone/>
    <Page3bottom/>
  </div>
</template>

<script>
import Page3header from './Page3header.vue'
import Page3videoplayer from './Page3videoplayer.vue'
import Page3rightzone from './Page3rightzone.vue'
import Page3leftzone from './Page3leftzone.vue'
import Page3bottom from './Page3bottom.vue'
export default {
  name: "HelloWorld",
  components:{
    Page3header,
    Page3videoplayer,
    Page3rightzone,
    Page3leftzone,
    Page3bottom
  }
};

</script>

<style scoped>
  .videoplayer{
    position: absolute;
    top: 50px;
    left:250px;
    right:350px;
    bottom:110px;
  }
  .header {
    margin-bottom:0;
    position: absolute;
    line-height: 150px;
    top: 0px;
    left: 0px;
    right: 0px;
    background-color: transparent;
  }
  
  .rightzone{
    margin-bottom:0;
    position: absolute;
    text-align:center;
    width: 350px;
    top: 50px;  
    right: 0px;
    bottom: 110px; 
    /* overflow-y: auto;  */
    background-color: #409EFF;
  }
  .leftzone {
    position: absolute;
    margin-bottom:0;
    text-align:center;
    width: 100px;
    top: 50px; 
    left: 0px;
    bottom: 0px;
    overflow-y: auto; 
    background-color:transparent;
  }
  
  /* 主区域 */
  .bottom {
    margin-bottom:0;
    position: absolute;
    text-align:center;
    top: 510px;
    left: 0px;
    bottom: 0px;
    height: 120px;
    right: 0px; 
    padding: 10px;
    background-color: #909399;
  }
  </style>
 