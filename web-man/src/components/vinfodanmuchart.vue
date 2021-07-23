<template>
  <div style="width: 100%; height: 350px">
    <div id="label5" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
var tempuse = "BV1144y1q7ve";
import Bus from ".././bus.js";
import config from "./../config";

const chartColors = config.app.chartColors;
const { axisColor } = chartColors;

let lineColors = [
  "rgb(255, 70, 131)",
  "rgb(255, 70, 131)",
  "rgb(255, 70, 131)",
];
export default {
  name: "vinfodanmuchart",
  data() {
    return {};
  },
  methods: {
    ttt() {
      this.draw();
    },
    draw() {
      var myChart = this.$echarts.init(
        document.getElementById("label5"),
        "infographic"
      );
      myChart.setOption({
        color: lineColors,
        tooltip: {
          trigger: "none",
          axisPointer: {
            type: "cross",
          },
        },
        grid: {
          x: 50,
          top: 50,
          bottom: 80,
          height: 250,
          width: 570,
        },
        xAxis: [
          {
            type: "value",
            axisTick: {
              alignWithLabel: true,
            },
            axisLine: {
              onZero: false,
              lineStyle: {
                color: axisColor,
              },
            },
            axisPointer: {
              label: {
                formatter: function (params) {
                  return (
                    "Precipitation  " +
                    params.value +
                    (params.seriesData.length
                      ? "：" + params.seriesData[0].data
                      : "")
                  );
                },
              },
            },
          },
          {
            type: "value",
            axisTick: {
              alignWithLabel: true,
            },
            axisLine: {
              onZero: false,
              lineStyle: {
                color: axisColor,
              },
            },
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              color: axisColor,
            },
            axisLine: {
              lineStyle: {
                color: axisColor,
              },
            },
          },
        ],
        series: [
          {
            name: "弹幕量",
            type: "line",
            xAxisIndex: 1,
            smooth: true,
            data: [],
          },
        ],
      });
      this.$http
        .get(
          "http://131.mollnn.com:5000/api/v/danmu/distrib/" + tempuse + "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          myChart.hideLoading();
          myChart.setOption({ series: [{ data: res.data }] });
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