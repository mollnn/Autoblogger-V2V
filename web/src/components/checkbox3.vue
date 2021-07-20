<template>
  <el-select v-model="value" placeholder="请选择视频源类型">
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
      options: [
        {
          value: "0",
          label: "电影",
        },
        {
          value: "1",
          label: "其他",
        },
      ],
      value: "",
    };
  },
};
</script>