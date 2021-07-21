<template>
  <div class="bottom">
    <swiper :options="swiperOption" ref="mySwiper">
      <swiper-slide
        class="swiper-slide"
        v-for="(item, index) in collocateContentDtos"
        :key="index"
        @click.native="changevideo(index)"
      >
        <img :src="item" width="100%" />
        <!--          @click.native="goJump(item)" 每一个图片的点击事件-->
        <!-- <div class="bs-swiper-bottom">
          <div>{{item.desc}}</div>
            <div>{{item.date}}</div>
        </div> -->
      </swiper-slide>
      <div class="swiper-button-prev" slot="button-prev"></div>
      <div class="swiper-button-next" slot="button-next"></div>
    </swiper>
  </div>
</template>

<script>
// 引入插件
import Bus from "../bus1.js";
import { swiper, swiperSlide } from "vue-awesome-swiper";
import "swiper/dist/css/swiper.css";

export default {
  components: {
    swiper,
    swiperSlide,
  },
  methods: {
    changevideo: function (e) {
      this.$store.state.vlink = this.$store.state.videolist[e];
      Bus.$emit("changevideo", this.$store.state.vlink);
      // this.swiper.slideTo(this.$store.state.index + 1, 1000, false)
      this.swiper.slideTo(this.$store.state.index - 0);
      this.$forceUpdate();
    },
  },
  data() {
    return {
      collocateContentDtos: [
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片1",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片2",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片3",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-2.jpg",
          desc: "图片4",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片5",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-4.jpg",
          desc: "图片6",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片7",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片8",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-1.jpg",
          desc: "图片9",
          date: "2020-01-05",
        },
        {
          image: "https://img.yzcdn.cn/vant/apple-3.jpg",
          desc: "图片10",
          date: "2020-01-05",
        },
      ],

      swiperOption: {
        
        effect: "coverflow",
        coverflowEffect: {
          rotate: -3,
          stretch: 330,
          depth: 300,
          modifier: 1,
          reverseDirection: true,
          // mousewheel: true,
          slideShadows: true,
        },

        centeredSlides: true,
        initialSlide: 12,
        slidesPerView: 7, //一行显示4个
        spaceBetween: 30, //间隔30
        // freeMode: true,
        speed: 1000, //滑动速度
        navigation: {
          nextEl: ".swiper-button-pre",
          prevEl: ".swiper-button-next",
        },
        autoHeight: true,
        // on: {
        //   click: (e) => {
        //     this.$store.state.vlink = e;
        //   },
        // },
      },
    };
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.swiper;
    },
  },
  mounted() {
    
    console.log("Current this instance object", this);
    console.log("Current Swiper instance object", this.swiper);
    this.collocateContentDtos = this.$store.state.posterlist.reverse();
    this.$store.state.videolist= this.$store.state.videolist.reverse();
    // this.collocateContentDtos = this.$store.state.posterlist;
    this.$forceUpdate();
    this.swiper.slideTo(this.$store.state.index - 0);
    Bus.$on("changethebottom", (val) => {
      this.swiper.slideTo(val - 0, 500);
    });
  },
};
</script>
<style scoped >
.swiper-container {
  width: 100%;
  height: 100%;
  padding: 0px;
}
.swiper-slide {
  width: 30%;
  height: 100%;
  position: relative;
}
.bs-swiper-bottom {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 0px;
  background-color: rgba(65, 105, 225, 0.7);
  color: #fff;
  font-size: 10px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>

