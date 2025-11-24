<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h2>数据集列表</h2>
      </div>
    </template>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-if="error" class="error-state">
      <el-alert :title="error" type="error" show-icon :closable="false"></el-alert>
    </div>

    <div v-if="!loading && !error" class="dataset-list">
      <el-card v-for="dataset in datasets" :key="dataset.id" class="dataset-item" shadow="hover">
        <el-row :gutter="20" align="middle">
          <el-col :span="6">
            <el-image 
              style="width: 100%; height: 120px; border-radius: 4px;"
              :src="dataset.imageUrl" 
              fit="cover"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon :size="30"><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </el-col>
          <el-col :span="18">
            <h3>{{ dataset.name }}</h3>
            <p class="description">{{ dataset.description }}</p>
            <a :href="dataset.downloadUrl" :download="dataset.name">
              <el-button type="primary">
                <el-icon class="el-icon--left"><Download /></el-icon>
                下载数据集
              </el-button>
            </a>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Picture, Download } from '@element-plus/icons-vue';

// Define the interface for a dataset item for type safety
interface Dataset {
  id: number;
  name: string;
  description: string;
  imageUrl: string;
  downloadUrl: string;
}

const datasets = ref<Dataset[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    // Fetch the static JSON file from the public folder
    const response = await fetch('/datasets.json');
    if (!response.ok) {
      throw new Error(`网络错误: ${response.statusText}`);
    }
    datasets.value = await response.json();
  } catch (err) {
    if (err instanceof Error) {
        console.error('获取数据集失败:', err.message);
        error.value = `无法加载数据集列表: ${err.message}`;
    } else {
        console.error('未知错误:', err);
        error.value = '无法加载数据集列表，请稍后重试。';
    }
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.card-header {
  text-align: center;
}
.loading-state, .error-state {
  padding: 40px 20px;
  text-align: center;
}
.dataset-list .dataset-item {
  margin-bottom: 20px;
}
.dataset-item h3 {
  margin-top: 0;
  margin-bottom: 8px;
}
.dataset-item .description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  min-height: 40px;
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: var(--el-text-color-secondary);
}
a {
  text-decoration: none;
}
</style>