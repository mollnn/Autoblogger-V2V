<template>
  <div>
    <h2>选择你想要的视频源类别</h2>
    <input type="checkbox" value="电影" v-model="type1" />电影<br />
    <input type="checkbox" value="其他" v-model="type1" />其他
    <h2>选择你想要的视频内容分类</h2>
    <input type="checkbox" value="弹幕密集" v-model="type2" />弹幕密集<br />
    <input type="checkbox" value="高能打斗" v-model="type2" />高能打斗<br /><br /><br />
    <router-link to="/page2" tag = "button" type = "primary">Submit</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      type1: [],
      type2: [],
    };
  },
};
</script>

