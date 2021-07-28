<template>
  <div class="table-resposive">
    <table class="table">
      <thead>
        <tr>
          <th class="hidden-sm-down">排名</th>
          <th class="hidden-sm-down">BVID</th>
          <th>标题</th>
          <th>分区</th>
          <th class="hidden-sm-down">时长</th>
          <th class="hidden-sm-down">总播放量</th>
          <th class="hidden-sm-down">总弹幕数</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in slist" :key="index">
          <td>{{ index + 1 }}</td>
          <td>
            {{ item[0] }}
          </td>
          <td>
            {{ item[1] }}
          </td>
          <td>
            {{ item[2] }}
          </td>
          <td>
            {{ item[3] }}
          </td>
          <td>
            {{ item[4] }}
          </td>
          <td>
            {{ item[5] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "vinfotable",
  data() {
    return { slist: [] };
  },
  methods: {
    ttt() {
      this.draw();
    },
    draw() {
      this.$http
        .get("http://v2v.mollnn.com:5000/api/vrank/", {
          headers: { "Access-Control-Allow-Origin": "*" },
        })
        .then((res) => {
          this.slist = res.data;
          this.$forceUpdate();
        });
    },
  },
  mounted() {
    this.draw();
  },
};
</script>

<style></style>
