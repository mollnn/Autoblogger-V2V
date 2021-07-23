<template>
  <div style="width: 100%; height: 300px">
    <div id="echartContainer9" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
import echarts from "echarts";
export default {
  name: "coinchart",
  data() {
    return {};
  },
  methods: {
    draw() {
      var myChart = this.$echarts.init(
        document.getElementById("echartContainer9"),
        "infographic"
      );
      myChart.setOption({
        tooltip: {
          trigger: "axis",
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        calculable: true,
        xAxis: [
          {
            type: "value",
            max: 10000,
            splitLine: { show: false },
            axisLine: {
              show: false,
            },

            axisTick: {
              show: false,
            },
            axisLabel: {
              textStyle: {
                fontSize: 8,
                color: "#999",
              },
              rotate: -20,

              z: 10,
            },
          },
        ],
        yAxis: [
          {
            type: "value",
            splitLine: { show: false },
            axisLine: {
              show: false,
            },
            axisTick: {
              show: false,
            },
            axisLabel: {
              textStyle: {
                fontSize: 8,
                color: "#999",
              },
            },
          },
        ],
        dataZoom: [
          {
            type: "inside",
          },
        ],
        series: [
          {
            showBackground: true,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "rgb(255, 70, 131)" },
                { offset: 0.5, color: "rgb(255, 158, 68)" },
                { offset: 1, color: "rgb(255, 158, 68)" },
              ]),
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#F55555" },
                  { offset: 0.7, color: "#F55555" },
                  { offset: 1, color: "#F55555" },
                ]),
              },
            },
            name: "视频量",
            type: "bar",
            data: [],
          },
        ],
        grid: [
          {
            top: 10,
            bottom: 23.5,
            left: "14%",
            right: "11%",
          },
        ],
      });
      // Enable data zoom when user click bar.

      this.$http
        .get("http://131.mollnn.com:5000/api/coin/distrib/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          myChart.hideLoading();
          myChart.setOption({ series: [{ data: res.data }] });
        });
    },
  },
  mounted() {
    this.draw();
  },
};
</script>

<style></style>








