<template>
  <div class="tables-basic">
    <h1 class="page-title">管线状态监控<span class="fw-semi-bold"></span></h1>
    <b-row>
      <b-col lg="6">
        <Widget customHeader settings close>
          <h3>管线状态概览 <span class="fw-semi-bold"></span></h3>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>状态</th>
                  <th>总进度</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ ssx }}</td>
                  <td>{{ ssy }} %</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Widget>
        <Widget customHeader settings close>
          <h3>媒体对象载入段 <span class="fw-semi-bold"></span></h3>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>BVID</th>
                  <th>进度</th>
                </tr>
              </thead>
              <tbody>
                <tr v-cloak v-for="(item, index) of alist" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item[0] }}</td>
                  <td>{{ item[1] }} %</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Widget>
      </b-col>
      <b-col lg="6">
        <Widget customHeader settings close>
          <h3>定制化媒体切片提取段<span class="fw-semi-bold"></span></h3>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>BVID</th>
                  <th>进度</th>
                </tr>
              </thead>
              <tbody>
                <tr v-cloak v-for="(item, index) of blist" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item[0] }}</td>
                  <td>{{ item[1] }} %</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Widget>
        <Widget customHeader settings close>
          <h3>媒体子对象合成段 <span class="fw-semi-bold"></span></h3>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>OVID</th>
                  <th>进度</th>
                </tr>
              </thead>
              <tbody>
                <tr v-cloak v-for="(item, index) of clist" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item[0] }}</td>
                  <td>{{ item[1] }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Widget>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Vue from "vue";
import Widget from "@/components/Widget/Widget";
import Sparklines from "../../components/Sparklines/Sparklines";

export default {
  name: "Tables",
  components: { Widget, Sparklines },
  data() {
    return {
      timer: null,
      alist: [],
      blist: [],
      clist: [],
      ssx: "",
      ssy: "",
      tableStyles: [
        {
          id: 1,
          picture: require("../../assets/tables/1.jpg"), // eslint-disable-line global-require
          description: "Palo Alto",
          info: {
            type: "JPEG",
            dimensions: "200x150",
          },
          date: new Date("September 14, 2012"),
          size: "45.6 KB",
          progress: {
            percent: 29,
            colorClass: "success",
          },
        },
        {
          id: 2,
          picture: require("../../assets/tables/2.jpg"), // eslint-disable-line global-require
          description: "The Sky",
          info: {
            type: "PSD",
            dimensions: "2400x1455",
          },
          date: new Date("November 14, 2012"),
          size: "15.3 MB",
          progress: {
            percent: 33,
            colorClass: "warning",
          },
        },
        {
          id: 3,
          picture: require("../../assets/tables/3.jpg"), // eslint-disable-line global-require
          description: "Down the road",
          label: {
            colorClass: "danger",
            text: "INFO!",
          },
          info: {
            type: "JPEG",
            dimensions: "200x150",
          },
          date: new Date("September 14, 2012"),
          size: "49.0 KB",
          progress: {
            percent: 38,
            colorClass: "inverse",
          },
        },
        {
          id: 4,
          picture: require("../../assets/tables/4.jpg"), // eslint-disable-line global-require
          description: "The Edge",
          info: {
            type: "PNG",
            dimensions: "210x160",
          },
          date: new Date("September 15, 2012"),
          size: "69.1 KB",
          progress: {
            percent: 17,
            colorClass: "danger",
          },
        },
        {
          id: 5,
          picture: require("../../assets/tables/5.jpg"), // eslint-disable-line global-require
          description: "Fortress",
          info: {
            type: "JPEG",
            dimensions: "1452x1320",
          },
          date: new Date("October 1, 2012"),
          size: "2.3 MB",
          progress: {
            percent: 41,
            colorClass: "primary",
          },
        },
      ],
      checkboxes1: [false, false, false, false],
      checkboxes2: [false, false, false, false, false, false],
      checkboxes3: [false, false, false, false, false, false],
    };
  },
  mounted() {
    this.draw1();
    this.draw2();
    this.draw3();
    this.timer = setInterval(() => {
      setTimeout(this.draw1(), 0);
    }, 1000 * 2);
    this.timer = setInterval(() => {
      setTimeout(this.draw2(), 0);
    }, 1000 * 2);
    this.timer = setInterval(() => {
      setTimeout(this.draw3(), 0);
    }, 1000 * 2);
  },
  methods: {
    draw1() {
      console.log("fuck");
      this.$http
        .get("http://v2v.mollnn.com:5000/api/status/load/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.alist = res.data;
          this.$forceUpdate();
        });
    },
    draw2() {
      console.log("fuck");
      this.$http
        .get("http://v2v.mollnn.com:5000/api/status/extract/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.blist = res.data;
          this.$forceUpdate();
        });
    },
    draw3() {
      console.log("fuck");
      this.$http
        .get("http://v2v.mollnn.com:5000/api/status/generate/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.clist = res.data;
          this.$forceUpdate();
        });
              this.$http
        .get("http://v2v.mollnn.com:5000/api/status/pipeline/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.ssx = res.data;
          this.$forceUpdate();
        });
      this.$http
        .get("http://v2v.mollnn.com:5000/api/status/progress/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.ssy = res.data;
          this.$forceUpdate();
        });
    },
    parseDate(date) {
      const dateSet = date.toDateString().split(" ");
      return `${date.toLocaleString("en-us", { month: "long" })} ${
        dateSet[2]
      }, ${dateSet[3]}`;
    },
    checkAll(ev, checkbox) {
      const checkboxArr = new Array(this[checkbox].length).fill(
        ev.target.checked
      );
      Vue.set(this, checkbox, checkboxArr);
    },
    changeCheck(ev, checkbox, id) {
      this[checkbox][id] = ev.target.checked;
      if (!ev.target.checked) {
        this[checkbox][0] = false;
      }
    },
    getRandomData() {
      const result = [];

      for (let i = 0; i <= 8; i += 1) {
        result.push(Math.floor(Math.random() * 20) + 1);
      }

      return [{ data: result }];
    },
    getRandomColor() {
      const { primary, success, info, danger } = this.appConfig.colors;
      const colors = [info, primary, danger, success];
      return { colors: [colors[Math.floor(Math.random() * colors.length)]] };
    },
  },
  beforeDestroy() {
    clearInterval(this.timer);
    this.timer = null;
  },
};
</script>

<style src="./Basic.scss" lang="scss" scoped />
