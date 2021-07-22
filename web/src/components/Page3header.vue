<template>
  <div class="header">
    <el-page-header @back="goBack" content="V2V视频播放..."> </el-page-header>
  </div>
</template>
<script>
export default {
  methods: {
    goBack() {
      this.$router.push('/page2')
    },
  },
};
</script>