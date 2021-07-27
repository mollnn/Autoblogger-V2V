<template>
  <div>
    <h1 class="page-title">管线管理 <span class="fw-semi-bold"></span></h1>
    <b-row>
      <b-col xs="12" lg="6">
        <Widget customHeader close collapse>
          <h4>源素材管理</h4>
          <br />
          <b-row>
            <form class="form-inline" role="form">
              <div class="form-group">
                <span style="padding: 14px"></span>
                <input
                  type="text"
                  placeholder="关键词搜索"
                  class="form-control"
                  v-model="msgaa"
                />
                <span style="padding: 10px"></span>
                <input
                  type="text"
                  placeholder="BVID"
                  class="form-control"
                  v-model="msg1"
                />
              </div>
              <span style="padding: 5px"></span>
            </form>
            <br />

            <form class="form-inline" role="form">
              <span style="padding: 14px"></span>
              <button type="button" @click="addinfo1" class="btn btn-primary">
                添加素材信息
              </button>
              <span style="padding: 26px"></span>
              <button
                type="button"
                @click="clearsource"
                class="btn btn-primary"
              >
                清空素材信息
              </button>
            </form>
            <br />
          </b-row>
          <table class="table">
            <thead>
              <tr>
                <th>序号</th>
                <th>BVID</th>
                <th>删除按钮</th>
              </tr>
            </thead>
            <tbody>
              <tr v-cloak v-for="(item, index) of slist" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item[0] }}</td>
                <td>
                  <a href="javascript:;" @click="del1(index)">删除</a>
                </td>
              </tr>
            </tbody>
          </table>
        </Widget>
      </b-col>
      <b-col xs="12" lg="6">
        <Widget customHeader close collapse>
          <h4>模板管理</h4>
          <b-row>
            <form class="form-inline" role="form">
              <span style="padding: 24px"></span>
              <input
                type="text"
                placeholder="关键词搜索"
                class="form-control"
                v-model="msgbb"
              />
              <span style="padding: 14px"></span>
              <input
                type="text"
                placeholder="BVID"
                class="form-control"
                v-model="msg3"
              />
            </form>
            <br /><br />
            <form class="form-inline" role="form">
              <span style="padding: 24px"></span>
              <input
                type="text"
                placeholder="tag"
                class="form-control"
                v-model="msg5"
              />
            </form>
            <form class="form-inline" role="form">
              <span style="padding: 14px !important"></span>
              <button type="button" @click="addinfo2" class="btn btn-primary">
                添加
              </button>
              <span style="padding: 10px"></span>
              <button type="button" @click="execall" class="btn btn-primary">
                执行
              </button>
            </form>
            <form class="form-inline" role="form">
              <span style="padding: 10px"></span>
              <button
                type="button"
                @click="cleartemplate"
                class="btn btn-primary"
              >
                清空
              </button>
            </form>
          </b-row>
          <table class="table">
            <thead>
              <tr>
                <th>序号</th>
                <th>BVID</th>
                <th>类型号</th>
                <th>删除按钮</th>
              </tr>
            </thead>
            <tbody>
              <tr v-cloak v-for="(item, index) of blist" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item[0] }}</td>
                <td>{{ item[2] }}</td>
                <td>
                  <a href="javascript:;" @click="del2(index)">删除</a>
                </td>
              </tr>
            </tbody>
          </table>
        </Widget>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Widget from "@/components/Widget/Widget";

export default {
  name: "Typography",
  components: { Widget },
  mounted() {
    this.draw1();
    this.draw2();
  },
  methods: {
    execall() {
      this.$forceUpdate();
      this.$http
        .get("http://v2v.mollnn.com:5000/api/exec/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
        });
      alert("正在执行....");
    },
    del1(index) {
      this.$forceUpdate();
      this.$http
        .get(
          "http://v2v.mollnn.com:5000/api/source/delete/" +
            this.slist[index][0] +
            "/" +
            this.slist[index][1] +
            "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          this.draw1();
          console.log(res);
          this.$forceUpdate();
        });
    },
    addinfo1() {
      if (this.msgaa == "" && this.msg1 == "") {
        alert("格式错误，请重新填写！");
        return;
      } else if (this.msgaa != "" && this.msg1 != "") {
        alert("格式错误，请重新填写！");
        return;
      } else {
        if (this.msgaa == "") {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/source/insert/" + this.msg1 + "/",
              {
                headers: { "Access-Control-Allow-Origin": "*" },
              }
            )
            .then((res) => {
              console.log(res);
              this.draw1();
              this.$forceUpdate();
            });
        } else {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/source/searchinsert/" +
                this.msgaa +
                "/",
              {
                headers: { "Access-Control-Allow-Origin": "*" },
              }
            )
            .then((res) => {
              console.log(res);
              this.draw1();
              this.$forceUpdate();
            });
        }
        this.msg1 = "";
        this.msgaa = "";
      }
    },
    draw1() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/source/query/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.slist = res.data;
          this.$forceUpdate();
        });
    },
    clearsource() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/source/clear/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.draw1();
          this.$forceUpdate();
        });
    },
    del2(index) {
      this.$forceUpdate();
      this.$http
        .get(
          "http://v2v.mollnn.com:5000/api/template/delete/" +
            this.blist[index][0] +
            "/" +
            this.blist[index][1] +
            "/" +
            this.blist[index][2] +
            "/",
          {
            headers: { "Access-Control-Allow-Origin": "*" },
          }
        )
        .then((res) => {
          this.draw2();
          console.log(res);
          this.$forceUpdate();
        });
    },
    addinfo2() {
      if (this.msg5 == "") {
        alert("格式错误，请重新填写！");
        return;
      } else if (this.msgbb == "" && this.msg3 == "") {
        alert("格式错误，请重新填写！");
        return;
      } else if (this.msgbb != "" && this.msg3 != "") {
        alert("格式错误，请重新填写！");
        return;
      } else {
        if (this.msgbb == "") {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/template/insert/" +
                this.msg3 +
                "/" +
                this.msg5 +
                "/",
              {
                headers: { "Access-Control-Allow-Origin": "*" },
              }
            )
            .then((res) => {
              console.log(res);
              this.draw2();
              this.$forceUpdate();
            });
        } else {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/template/searchinsert/" +
                this.msgbb +
                "/" +
                this.msg5 +
                "/",
              {
                headers: { "Access-Control-Allow-Origin": "*" },
              }
            )
            .then((res) => {
              console.log(res);
              this.draw2();
              this.$forceUpdate();
            });
        }
        this.msgbb = "";
        this.msg3 = "";
        this.msg5 = "";
      }
    },
    draw2() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/template/query/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.blist = res.data;
          this.$forceUpdate();
        });
    },
    cleartemplate() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/template/clear/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          console.log(res);
          this.draw2();
          this.$forceUpdate();
        });
    },
  },
  data() {
    return {
      slist: [],
      blist: [],
      msgaa: "",
      msgbb: "",
      msg1: "",
      msg3: "",
      msg5: "",
    };
  },
};
</script>
