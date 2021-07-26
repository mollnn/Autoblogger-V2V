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
          value: "1",
          label: "热点",
        },
        {
          value: "2",
          label: "高甜",
        },
        {
          value: "3",
          label: "养眼",
        },
        {
          value: "4",
          label: "幽默",
        },
      ],
      value: "",
    };
  },
};
</script>