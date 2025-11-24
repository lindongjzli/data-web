<template>
  <el-container>
    <el-header>
      <NavBar />
    </el-header>
    <el-main>
      <el-row justify="center">
        <el-col :xs="24" :sm="20" :md="16" :lg="14">
          <RouterView />
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>

<style>
/* Global styles can go here */
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.el-main {
  padding-top: 40px;
}
</style>
