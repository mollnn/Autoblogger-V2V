<template>
  <div class="rightzone">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>视频信息概要</span>
        <el-button style="float: right; padding: 3px 0" type="text"
          >点击查看详情</el-button
        >
      </div>
      <div v-for="o in 8" :key="o" class="text item">
        {{ "视频信息条目 " + o }}
      </div>
    </el-card>
  </div>
</template>


<style>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 350px;
  right:0px;
}
</style>