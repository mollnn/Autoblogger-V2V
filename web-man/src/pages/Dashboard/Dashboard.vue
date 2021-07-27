<template>
  <div class="dashboard-page">
    <h1 class="page-title">热点数据总览</h1>
    <b-row>
      <b-col md="6" xl="3" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频播放总数" close>
            <sumlabel />
          </Widget>
        </div>
      </b-col>
      <b-col md="6" xl="3" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频收藏分布" close>
            <favoritechart style="height: 175px"></favoritechart>
          </Widget>
        </div>
      </b-col>
      <b-col md="6" xl="3" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频点赞分布" close>
            <likeschart style="height: 175px"></likeschart>
          </Widget>
        </div>
      </b-col>
      <b-col md="6" xl="3" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频投币分布" close>
            <coinchart style="height: 175px"></coinchart>
          </Widget>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6" xl="4" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频播放分布" close>
            <viewchart style="height: 175px"></viewchart>
          </Widget>
        </div>
      </b-col>
      <b-col md="6" xl="4" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频时间分布" close>
            <durationchart style="height: 175px"></durationchart>
          </Widget>
        </div>
      </b-col>
      <b-col md="6" xl="4" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="视频评论分布" close>
            <replychart style="height: 175px"></replychart>
          </Widget>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6" xl="6" sm="6" xs="12">
        <Widget
          title="<h5> Blibli <span class='fw-semi-bold'>实时用户数量</span></h5>"
          close
          collapse
          customHeader
        >
          <highcharts :options="ld" ref="highchart"></highcharts>
        </Widget>
      </b-col>
      <b-col md="6" xl="6" sm="6" xs="12">
        <div class="pb-xlg h-100">
          <Widget class="h-100 mb-0" title="类型分布" close>
            <typechart style="height: 250px"></typechart>
          </Widget>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Widget from "@/components/Widget/Widget";
import BigStat from "./components/BigStat/BigStat";
import { chartData, liveChart, liveChartInterval } from "./mock";
import mock from "./mock";
import ECharts from "vue-echarts/components/ECharts";
import Highcharts from "highcharts";
import exporting from "highcharts/modules/exporting";
import exportData from "highcharts/modules/export-data";
import "echarts/lib/chart/pie";
import "echarts/lib/chart/line";
import "echarts/lib/chart/themeRiver";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/legend";
import viewchart from "@/components/viewchart";
import durationchart from "@/components/durationchart";
import replychart from "@/components/replychart";
import typechart from "@/components/typechart";
import favoritechart from "@/components/favoritechart";
import likeschart from "@/components/likeschart";
import coinchart from "@/components/coinchart";
import sumlabel from "@/components/sumlabel";
import { Chart } from "highcharts-vue";

exporting(Highcharts);
exportData(Highcharts);
exporting(Highcharts);
exportData(Highcharts);

export default {
  name: "Dashboard",
  components: {
    viewchart,
    durationchart,
    replychart,
    typechart,
    favoritechart,
    likeschart,
    coinchart,
    sumlabel,
    Widget,
    BigStat,
    echart: ECharts,
    highcharts: Chart,
    initEchartsOptions: {
      renderer: "canvas",
    },
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
  methods: {
    getRandomData() {
      const arr = [];
      for (let i = 0; i < 25; i += 1) {
        arr.push(Math.random().toFixed(1) * 10);
      }
      return arr;
    },
    getRevenueData() {
      const data = [];
      const seriesCount = 3;
      const accessories = ["SMX", "Direct", "Networks"];

      for (let i = 0; i < seriesCount; i += 1) {
        data.push({
          label: accessories[i],
          data: Math.floor(Math.random() * 100) + 1,
        });
      }

      return data;
    },
  },
  computed: {
    donut() {
      let revenueData = this.getRevenueData();
      let { danger, info, primary } = this.appConfig.colors;
      let series = [
        {
          name: "Revenue",
          data: revenueData.map((s) => {
            return {
              name: s.label,
              y: s.data,
            };
          }),
        },
      ];
      return {
        chart: {
          type: "pie",
          height: 120,
        },
        credits: {
          enabled: false,
        },
        title: false,
        plotOptions: {
          pie: {
            dataLabels: {
              enabled: false,
            },
            borderColor: null,
            showInLegend: true,
            innerSize: 60,
            size: 100,
            states: {
              hover: {
                halo: {
                  size: 1,
                },
              },
            },
          },
        },
        colors: [danger, info, primary],
        legend: {
          align: "right",
          verticalAlign: "middle",
          layout: "vertical",
          itemStyle: {
            color: "#495057",
            fontWeight: 100,
            fontFamily: "Montserrat",
          },
          itemMarginBottom: 5,
          symbolRadius: 0,
        },
        exporting: {
          enabled: false,
        },
        series,
      };
    },
  },
  beforeDestroy() {
    clearInterval(liveChartInterval);
  },
};
</script>

<style src="./Dashboard.scss" lang="scss" />
