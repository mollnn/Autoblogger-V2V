<template>
  <div>
    <h1 class="page-title">
      Typography - <span class="fw-semi-bold">Texts & Display</span>
    </h1>
    <b-row>
      <b-col xs="12" lg="6">
        <Widget
          title="<h5>Headings <small class='text-muted'>Default and customized</small></h5>"
          customHeader
          close
          collapse
        >
          <h4>Table1---</h4>
          <b-row>
            <form class="form-inline" role="form">
              <div class="form-group">
                <span style = "padding : 24px"></span>
                <input
                  type="text"
                  placeholder="输入搜素信息"
                  class="form-control"
                  v-model="msgaa"
                />
                <span style = "padding : 14px"></span>
                <input
                  type="text"
                  placeholder="输入添加信息1"
                  class="form-control"
                  v-model="msg1"
                />
              </div>
            </form>
            <form class="form-inline" role="form">
              <span style = "padding : 24px"></span>
              <input
                type="text"
                placeholder="输入添加信息2"
                class="form-control"
                v-model="msg2"
              />
              <span style = "padding : 14px"></span>
              <button type="button" @click="addinfo1" class="btn btn-primary">
                添加信息
              </button>
            </form>
          </b-row>
          <table class="table">
            <thead>
              <tr>
                <th>id</th>
                <th>Bid</th>
                <th>info</th>
                <th>删除按钮</th>
              </tr>
            </thead>
            <tbody>
              <tr v-cloak v-for="(item, index) of slist" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>
                  <a href="javascript:;" @click="del1(index)">删除</a>
                </td>
              </tr>
            </tbody>
          </table>
        </Widget>
      </b-col>
      <b-col xs="12" lg="6">
        <Widget
          title="<h5>Headings <small class='text-muted'>Default and customized</small></h5>"
          customHeader
          close
          collapse
        >
          <h4>Table2---</h4>
          <b-row>
            <form class="form-inline" role="form">
              <span style = "padding : 24px"></span>
            <input
              type="text"
              placeholder="输入搜索信息"
              class="form-control"
              v-model="msgbb"
            />
            <span style = "padding : 14px"></span>
            <input
              type="text"
              placeholder="输入添加信息3"
              class="form-control"
              v-model="msg3"
            />
            </form>
            <br><br>
            <form class="form-inline" role="form">
              <span style = "padding : 24px"></span>
            <input
              type="text"
              placeholder="输入添加信息5"
              class="form-control"
              v-model="msg5"
            />
            </form>
            <form class="form-inline" role="form">
              <span style = "padding : 14px !important"></span>
            <button type="button" @click="addinfo2" class="btn btn-primary">
              添加信息
            </button>
            <span style = "padding :23px"></span>
            <button type="button" @click="execall" class="btn btn-primary">
              执行！
            </button>
            </form>
          </b-row>
          <table class="table">
            <thead>
              <tr>
                <th>id</th>
                <th>Bid</th>
                <th>info</th>
                <th>hhh</th>
                <th>删除按钮</th>
              </tr>
            </thead>
            <tbody>
              <tr v-cloak v-for="(item, index) of blist" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
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
      if (this.msg2 == "") {
        alert("fuckyou man! get the msg box all full!");
        return;
      } else if (this.msgaa == "" && this.msg1 == "") {
        alert("fuckyou man! get the msg box all full!");
        return;
      } else if (this.msgaa != "" && this.msg1 != "") {
        alert("fuckyou man! get the msg box all full!");
        return;
      } else {
        if (this.msgaa == "") {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/source/insert/" +
                this.msg1 +
                "/" +
                this.msg2 +
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
        } else {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/source/searchinsert/" +
                this.msgaa +
                "/" +
                this.msg2 +
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
        this.msg2 = "";
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
        alert("fuckyou man! get the msg box all full!!!!");
        return;
      } else if (this.msgbb == "" && this.msg3 == "") {
        alert("fuckyou man! get the msg box all full!!!!");
        return;
      } else if (this.msgbb != "" && this.msg3 != "") {
        alert("fuckyou man! get the msg box all full!!!!");
        return;
      } else {
        if (this.msgbb == "") {
          this.$http
            .get(
              "http://v2v.mollnn.com:5000/api/template/insert/" +
                this.msg3 +
                "/" +
                this.msg4 +
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
                this.msg4 +
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
        this.msg4 = "";
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
  },
  data() {
    return {
      slist: [],
      blist: [],
      msgaa: "",
      msgbb: "",
      msg1: "",
      msg2: "",
      msg3: "",
      msg4: 0,
      msg5: "",
    };
  },
};
</script>
