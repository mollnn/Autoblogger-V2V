<template>
  <div style="width: 100%; height: 60%">
    <div id="echartContainer10" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
var tempuse = "XV1626826803813670732987";
import Bus from "../bus1.js";
export default {
  name: "vinfodanmmuciyun",
  data() {
    return {};
  },
  methods: {
    ttt() {
      this.draw();
    },
    draw() {
      var myChart = this.$echarts.init(
        document.getElementById("echartContainer10"),
        "infographic"
      );
      myChart.setOption({
        // title: {
        //     text: '热点分析',
        //     // link: 'https://www.baidu.com/s?wd=' + encodeURIComponent('ECharts'),
        //     x: 'center',
        //     textStyle: {
        //         fontSize: 23
        //     }
        // },
        backgroundColor: "#222",
        tooltip: {
          show: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {
              iconStyle: {
                normal: {
                  color: "#FFFFFF",
                },
              },
            },
          },
        },
        series: [
          {
            // name: '热点分析',
            type: "wordCloud",
            // size: ['9%', '99%'],
            sizeRange: [6, 30],
            //textRotation: [0, 45, 90, -45],
            rotationRange: [-45, 90],
            shape: "circle",
            width: 1200,
            height: 999,
            textPadding: 0,
            autoSize: {
              enable: false,
              minSize: 6,
            },
            textStyle: {
              normal: {
                color: function () {
                  return (
                    "rgb(" +
                    [
                      Math.round(Math.random() * 40 + 195),
                      Math.round(Math.random() * 50 + 145),
                      Math.round(Math.random() * 50 + 160),
                    ].join(",") +
                    ")"
                  );
                },
              },
              emphasis: {
                shadowBlur: 10,
                shadowColor: "#333",
              },
            },
            data: [],
          },
        ],
      });
      tempuse = this.$store.state.objlist[this.$store.state.index].id;
      this.$http
        .get("http://131.mollnn.com:5001/xv/wordcloud/" + tempuse + "/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          myChart.hideLoading();
          myChart.setOption({ series: [{ data: res.data }] });
          myChart.setOption({ series: [{ data: { name: "hhh", value: 1 } }] });
        });
    },
  },
  mounted() {
    this.draw();
    Bus.$on("changethebottom", (val) => {
      console.log(val);
      this.draw();
    });
    Bus.$on("changevideo", (val) => {
      console.log(val);
      this.draw();
    });
  },
};
</script>

<style></style>