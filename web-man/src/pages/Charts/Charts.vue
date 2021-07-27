<template>
  <div class="charts-overview">
    <h1 class="page-title">
      热点视频信息
      <span class="fw-semi-bold"></span>
    </h1>
    <div>
      <b-row>
        <b-col md="6" xl="3" sm="6" xs="12">
          <div class="pb-xlg h-100">
            <Widget class="h-100 mb-0" title="播放量" close>
              <vinfolabel />
            </Widget>
          </div>
        </b-col>
        <b-col md="6" xl="6" sm="6" xs="12">
          <div class="pb-xlg h-100">
            <Widget class="h-100 mb-0" title="视频简介" close>
              <vinfodescslabel style="height = 175px" />
            </Widget>
          </div>
        </b-col>
        <b-col md="6" xl="3" sm="6" xs="12">
          <div class="pb-xlg h-100">
            <Widget class="h-100 mb-0" title="视频封面" close>
              <vinfophotolabel />
            </Widget>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col xs="12">
          <Widget
            title="<h5>视频信息</h5>"
            bodyClass="widget-table-overflow"
            customHeader
          >
            <vinfotable />
          </Widget>
        </b-col>
      </b-row>
      <b-row>
        <b-col xs="12" lg="6">
          <Widget title="<h5>弹幕时刻分布</h5>" close collapse customHeader>
            <vinfodanmuchart />
          </Widget>
        </b-col>
        <b-col xs="12" lg="6">
          <div class="pb-xlg h-100">
            <Widget class="h-100 mb-0" title="弹幕词云" close>
              <vinfodanmmuciyun style="height: 300px" />
            </Widget>
          </div>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import vinfodanmmuciyun from "@/components/vinfodanmmuciyun";
import vinfolabel from "@/components/vinfolabel";
import vinfodescslabel from "@/components/vinfodescslabel";
import vinfophotolabel from "@/components/vinfophotolabel";
import vinfotable from "@/components/vinfotable";
import vinfodanmuchart from "@/components/vinfodanmuchart";
import Widget from "@/components/Widget/Widget";
import { chartData, liveChart, liveChartInterval } from "./mock";
import ECharts from "vue-echarts/components/ECharts";
import "echarts/lib/chart/pie";
import "echarts/lib/chart/line";
import "echarts/lib/chart/themeRiver";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/legend";
import Highcharts from "highcharts";
import exporting from "highcharts/modules/exporting";
import exportData from "highcharts/modules/export-data";
import mock from "./mock";
import { Chart } from "highcharts-vue";
import Sparklines from "../../components/Sparklines/Sparklines";

exporting(Highcharts);
exportData(Highcharts);

export default {
  name: "Charts",
  components: {
    Widget,
    echart: ECharts,
    highcharts: Chart,
    Sparklines,
    vinfodanmmuciyun,
    vinfolabel,
    vinfodescslabel,
    vinfophotolabel,
    vinfotable,
    vinfodanmuchart,
  },
  data() {
    return {
      mock,
      cd: chartData,
      ld: liveChart,
      initEchartsOptions: {
        renderer: "canvas",
      },
    };
  },
  computed: {
    sparklineData() {
      return {
        series: [{ data: [1, 7, 3, 5, 7, 8] }],
        options1: {
          colors: [this.appConfig.colors.primary],
          plotOptions: {
            bar: {
              columnWidth: "50%",
            },
          },
        },
        options2: {
          colors: [this.appConfig.colors.info],
          plotOptions: {
            bar: {
              columnWidth: "50%",
            },
          },
        },
      };
    },
  },
  beforeDestroy() {
    clearInterval(liveChartInterval);
  },
};
</script>
