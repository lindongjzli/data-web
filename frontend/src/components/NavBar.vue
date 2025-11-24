<template>
  <el-menu mode="horizontal" :router="true">
    <el-menu-item index="0" style="font-weight: bold; font-size: 1.2em;">
      数据集平台
    </el-menu-item>
    <el-menu-item index="1" route="/">首页</el-menu-item>
    
    <div class="flex-grow" />

    <template v-if="authStore.isAuthenticated">
      <el-menu-item index="2" route="/dataset">数据下载</el-menu-item>
      <el-sub-menu index="3">
        <template #title>{{ authStore.user?.username || '用户' }}</template>
        <el-menu-item index="3-1" @click="handleLogout">退出登录</el-menu-item>
      </el-sub-menu>
    </template>
    <template v-else>
      <el-menu-item index="4" route="/login">登录</el-menu-item>
      <el-menu-item index="5" route="/register">注册</el-menu-item>
    </template>
  </el-menu>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const handleLogout = () => {
  authStore.logout();
};
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
</style>
