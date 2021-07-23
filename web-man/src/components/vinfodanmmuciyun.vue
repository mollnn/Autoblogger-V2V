<template>
  <div style="width: 100%; height: 230px">
    <div id="echartContainer10" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
var tempuse = "BV1144y1q7ve";
import Bus from ".././bus.js";
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
        backgroundColor: "#FFFFFF",
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
            sizeRange: [6, 110],
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
      this.$http
        .get(
          "http://131.mollnn.com:5000/api/v/danmu/wordcount/" + tempuse + "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          myChart.hideLoading();
          myChart.setOption({ series: [{ data: res.data }] });
          myChart.setOption({ series: [{ data: { name: "hhh", value: 1 } }] });
        });
    },
  },
  mounted() {
    Bus.$on("change", (val) => {
      tempuse = val;
      this.ttt();
    });
    this.draw();
  },
};
</script>

<style></style>