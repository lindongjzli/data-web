<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h2>数据集下载</h2>
      </div>
    </template>
    <div class="content">
      <p>您已登录，现在可以下载完整的数据集。</p>
      <p>点击下面的按钮开始下载。文件将以 .zip 格式提供。</p>
      <el-button 
        type="success" 
        @click="downloadDataset" 
        :loading="downloading" 
        size="large"
      >
        {{ downloading ? '正在准备文件...' : '下载数据集 (ZIP)' }}
      </el-button>
      <el-alert v-if="error" :title="error" type="error" show-icon class="error-alert"></el-alert>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import apiClient from '@/services/api';
import { ElMessage } from 'element-plus';

const downloading = ref(false);
const error = ref('');

const downloadDataset = async () => {
  downloading.value = true;
  error.value = '';
  try {
    const response = await apiClient.get('/dataset/download', {
      responseType: 'blob', // Important for file downloads
    });

    // Create a URL for the blob
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    // Extract filename from content-disposition header if available
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'dataset.zip'; // default filename
    if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch.length > 1) {
            filename = filenameMatch[1];
        }
    }
    
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();

    // Clean up
    link.remove();
    window.URL.revokeObjectURL(url);

    ElMessage.success('下载已开始！');

  } catch (err) {
    error.value = '下载失败。您可能需要重新登录。';
    console.error('Download failed:', err);
  } finally {
    downloading.value = false;
  }
};
</script>

<style scoped>
.card-header, .content {
  text-align: center;
}
.content p {
  margin-bottom: 20px;
}
.error-alert {
  margin-top: 20px;
}
</style>
