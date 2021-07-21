<template>
<div class="loading" v-bind:style = "styleobj"></div>
</template>

<script>
export default {
  name: 'Loading' ,// 定义的组件名称 使用时写法：loading
  data() {
    return {
        styleobj :{
            fontSize:'30px',
            color:'red',
        }
    }
  },
}
</script>

<style scoped>
.loading {
  position: fixed;
  left: 0;
  top: 0;
  background: url('https://tse2-mm.cn.bing.net/th/id/OIP-C.h0M8feTeQOU4vF1T51h1bgHaEK?pid=ImgDet&rs=1') center center no-repeat #fff;
  width: 100%;
  height: 100%;
  z-index: 1000;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 2.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0.8s;
}
.bounce-enter-active {
  animation: bounce-in .5s;
}
.bounce-leave-active {
  animation: bounce-in .5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
</style>

