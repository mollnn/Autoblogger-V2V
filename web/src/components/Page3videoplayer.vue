<template>
  <div class="videoplayer">
    <!-- <el-empty description="暂无信息"></el-empty> -->
    <video-player
      class="video-player vjs-custom-skin input_video "
      ref="videoPlayer"
      :playsinline="true"
      :options="playerOptions"
      @ended="onPlayerEnded($event)"

      id="fff"
    ></video-player>
  </div>
</template>
<script>
import Bus from "../bus1.js";
export default {
  computed:{
    vlink(){
      return this.$store.state.vlink
    },
  },
  methods: {
      onPlayerEnded(player) {
        
        console.log('player ended!', player);
        console.log(this.$store.state.index);
        this.playerOptions.sources[0].src=this.$store.state.videolist[(this.$store.state.index - 1 + this.$store.state.videolist.length)%this.$store.state.videolist.length];
        this.$store.state.index = (this.$store.state.index - 1 + this.$store.state.videolist.length) % this.$store.state.videolist.length;
        this.playerOptions.poster = this.$store.state.posterlist[this.$store.state.index];
        this.$forceUpdate();
        Bus.$emit("changethebottom", this.$store.state.index);
      },
  },
  data() {
    return {
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0], //播放速度
        autoplay: true, //如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 导致视频一结束就重新开始。
        preload: "auto", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: "zh-CN",
        aspectRatio: "16:8", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [
          {
            type: "video/mp4", //这里的种类支持很多种：基本视频格式、直播、流媒体等，具体可以参看git网址项目
            src: this.$store.state.vlink, //url地址
          },
        ],
        poster:this.$store.state.posterlist[this.$store.state.videolist.length-1-this.$store.state.index] , //你的封面地址
        // width: document.documentElement.clientWidth, //播放器宽度
        // height:20,
        // width:10,
        notSupportedMessage: "此视频暂无法播放，请稍后再试", //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true, //全屏按钮
        },
      },
    };
  },
  mounted() {
    console.log("videookkk!");
      Bus.$on("changevideo", (val) => {
      this.playerOptions.sources[0].src=val;
      for(var i = 0; i < this.$store.state.videolist.length; i++){
        if(val == this.$store.state.videolist[i]){
          this.$store.state.index = i;
          break;
        }
      }
      console.log(val);
      this.$forceUpdate();
    });
  },

};
</script>
<style>
    .input_video{
        margin: 0 auto;
    }
</style>