<template>
  <div class="tables-basic">
    <h1 class="page-title">精彩剪辑<span class="fw-semi-bold"></span></h1>
    <b-row>
      <b-col>
        <Widget
          title="<h5>成片 <span class='fw-semi-bold'>列表</span></h5>"
          customHeader
          settings
          close
        >
          <div class="table-resposive">
            <table class="table">
              <thead>
                <tr>
                  <th class="hidden-sm-down">序号</th>
                  <th>成片封面</th>
                  <th>成片标题</th>
                  <th class="hidden-sm-down">模板对象描述</th>
                  <th class="hidden-sm-down">分类标记号</th>
                  <th class="hidden-sm-down">查看视频</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in slist" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <img
                      class="img-rounded"
                      :src="photolist[index]"
                      alt=""
                      height="50"
                    />
                  </td>
                  <td>
                    {{ item[3] }}
                  </td>
                  <td class="text-semi-muted">
                    {{ item[1] }}
                  </td>
                  <td class="text-semi-muted">
                    {{ item[2] }}
                  </td>
                  <td class="width-150">
                    <a :href="videolist[index]">点击查看视频</a>
                  </td>
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
  name: "Notifications",
  components: { Widget, Sparklines },
  mounted() {
    this.draw();
  },
  data() {
    return {
      slist: [],
      photolist: [],
      videolist: [],
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
  methods: {
    draw() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/ov/list/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.slist = res.data;
          this.getphotos();
          this.getvideos();
          this.$forceUpdate();
        });
    },
    getphotos() {
      for (var i = 0; i < this.slist.length; ++i) {
        this.photolist.push(
          "http://v2v.mollnn.com:5000/api/ov/poster/" + this.slist[i][0] + "/"
        );
      }
    },
    getvideos() {
      for (var i = 0; i < this.slist.length; ++i) {
        this.videolist.push(
          "http://39.101.139.97:8081/edited/" + this.slist[i][0] + ".mp4"
        );
      }
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
};
</script>

<style src="./Basic.scss" lang="scss" scoped />
