<template>
  <div style="width: 100%; height: 300px">
    <div id="echartContainer2" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
import echarts from "echarts";
export default {
  name: "viewchart",
  data() {
    return {};
  },
  methods: {
    draw() {
      var myChart = this.$echarts.init(
        document.getElementById("echartContainer2"),
        "infographic"
      );
      myChart.setOption({
        tooltip: {
          trigger: "axis",
          position: function (pt) {
            return [pt[0], "10%"];
          },
        },
        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {},
          },
        },
        xAxis: {
          type: "log",
          logbase: 10,
          min: 100000,
          max: 3500000,
          boundaryGap: false,
          axisLabel: {
            type: "value",
            max: 10000,
            splitLine: { show: false },
            axisLine: {
              show: false,
            },
            textStyle: {
              //fontSize: 8,
              color: "#999",
            },

            z: 10,
          },
          splitLine: { show: false },
          axisLine: {
            show: false,
          },
          //show:false,
          axisTick: {
            show: false,
          },
        },
        yAxis: {
          type: "value",
          boundaryGap: false,
          axisLine: {
            show: false,
          },
          axisTick: {
            show: false,
          },
          axisLabel: {
            textStyle: {
              color: "#999",
            },
          },
        },
        dataZoom: [
          {
            type: "inside",
          },
        ],
        series: [
          {
            name: "播放量",
            type: "line",
            symbol: "none",
            sampling: "lttb",

            itemStyle: {
              color: "rgb(255, 158, 68)",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 1,
                  color: "rgb(255, 70, 131)",
                },
                {
                  offset: 0,
                  color: "rgb(255, 158, 68)",
                },
              ]),
            },
            data: [],
          },
        ],
        grid: [
          {
            top: 20,
            bottom: 25,
            left: "10%",
            right: "10%",
          },
        ],
      });

      // Enable data zoom when user click bar.

      this.$http
        .get("http://131.mollnn.com:5000/api/view/distrib/", {
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

