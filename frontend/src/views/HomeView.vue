<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h1>{{ info.title }}</h1>
      </div>
    </template>
    <div v-if="loading" v-loading="loading" style="height: 200px;"></div>
    <div v-else-if="error" class="error-text">
      无法加载数据集信息，请稍后重试。
    </div>
    <div v-else>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="描述">{{ info.description }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ info.version }}</el-descriptions-item>
        <el-descriptions-item label="作者">{{ info.author }}</el-descriptions-item>
        <el-descriptions-item label="引用信息">
          <el-tag size="small">Citation</el-tag>
          {{ info.citation }}
        </el-descriptions-item>
        <el-descriptions-item label="文件类型">
          <el-tag v-for="type in info.file_types" :key="type" style="margin-right: 5px;">
            {{ type }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <el-divider />
      <div class="center-content">
        <p>如需下载数据集，请先登录或注册。</p>
        <el-button type="primary" @click="$router.push('/login')">前往登录</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';

const loading = ref(true);
const error = ref(false);
const info = ref({
  title: '加载中...',
  description: '',
  version: '',
  author: '',
  citation: '',
  file_types: [],
});

onMounted(async () => {
  try {
    const response = await apiClient.get('/dataset/info');
    info.value = response.data;
  } catch (err) {
    console.error('Failed to fetch dataset info:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.card-header {
  text-align: center;
}
.error-text {
  color: #f56c6c;
  text-align: center;
}
.center-content {
  text-align: center;
  margin-top: 20px;
}
</style>
