<template>
  <div>
    <checkbox1 class="box" /><br /><br /><br /><br /><br />
    <checkbox2 class="box" />
    <el-button type="primary" round @click="gotolink" class="btn"
      >Let's go!</el-button
    >
  </div>
</template>

<script>
import checkbox1 from "./checkbox1.vue";
import checkbox2 from "./checkbox2.vue";
import Bus from "../bus1.js";
export default {
  data() {
    return {
      value: [],
    };
  },
  methods: {
    gotolink() {
      this.$router.push("/page2");
      this.value[0] = this.$children[0].value;
      this.value[1] = this.$children[1].value;
      var tmp = this.value;

      setTimeout(function () {
        Bus.$emit("change", tmp);
        console.log(tmp);
      }, 500);
    },
  },
  components: {
    checkbox1,
    checkbox2,
  },
};
</script>

<style scoped>
.btn {
  position: absolute;
  text-align: center;
  top: 480px;
  left: 600px;
  padding: 10px;
}
.box {
  text-align: center;
  top: 160px;
  left: 530px;
  padding: 10px;
  overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
}
</style>
