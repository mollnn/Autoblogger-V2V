<template>
  <div>
    <div id="echartContainer6" style="width: 100%; height: 300px"></div>
  </div>
</template>

<script>
export default {
  name: "typechart",
  data() {
    return {};
  },
  methods: {
    draw() {
      var myChart = this.$echarts.init(
        document.getElementById("echartContainer6"),
        "infographic"
      );
      myChart.setOption({
        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {},
          },
        },
        animationType: "scale",
        animationEasing: "elasticOut",
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b}: {c} ({d}%)",
          position: function (p) {
            //其中p为当前鼠标的位置
            return [p[0] + 10, p[1] - 10];
          },
        },
        legend: {
          orient: "vertical",
          x: "80%",
          itemWidth: 15,
          itemHeight: 15,
          itemGap: 7,
        },
        visualMap: {
          show: false,
          min: 80,
          max: 500,
          inRange: {
            colorLightness: [0.7, 0.8],
          },
        },
        series: [
          {
            name: "分类类别",
            type: "pie",
            radius: ["50", "70%"],
            center: ["50%", "40%"],
            avoidLabelOverlap: false,
            itemStyle: {
              color: "#F55555",
              shadowBlur: 20,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "20",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [],
          },
        ],
      });
      this.$http
        .get("http://131.mollnn.com:5000/api/type/distrib/", {
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
