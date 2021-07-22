<template>
  <el-select v-model="value" placeholder="请选择视频内容类型">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
      >
    </el-option>
  </el-select>
</template>

<script>
  export default {
    data() {
      return {
        options: [{
          value: '0',
          label: '弹幕密集'
        }, {
          value: '1',
          label: '高能打斗'
        }],
        value: ''
      }
    },
  methods: {
  },
  }
</script>