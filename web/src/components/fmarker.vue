<template>
<div class="block" style="line-height: 35px !important; text-align: right;">
  <span class="demonstration" style="color:#FFFFFF;line-height:20px !important;height: 20px !important;top:10px !important;">评个分吧~</span>
  <el-rate
    v-model="value2"
    ref="elrate"
    :colors="colors"
    @change="marked">
  </el-rate>
</div>
</template>

<script>
  export default {
    name: "fmarker",
    data() {
      return {
        value2: null,
        colors: ['#99A9BF', '#F7BA2A', '#FF9900']  // 等同于 { 2: '#99A9BF', 4: { value: '#F7BA2A', excluded: true }, 5: '#FF9900' }
      }
    },
    methods: {
      marked() {
        this.$notify({
          title: '评分成功',
          message: '评分' + this.value2 + '已提交！',
          type: 'success',
          position: 'top-left',
          offset: 50,
        });
      }
    }
  }
</script>