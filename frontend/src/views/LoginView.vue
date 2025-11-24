<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h2>用户登录</h2>
      </div>
    </template>
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="rules"
      label-width="80px"
      @submit.prevent="submitForm"
    >
      <el-form-item label="用户名" prop="username">
        <el-input v-model="loginForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="loginForm.password" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading">登录</el-button>
        <el-button @click="$router.push('/register')">没有账户？去注册</el-button>
      </el-form-item>
    </el-form>
    <el-alert v-if="error" :title="error" type="error" show-icon class="error-alert"></el-alert>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { FormInstance, FormRules } from 'element-plus';

const authStore = useAuthStore();
const loginFormRef = ref<FormInstance>();
const loading = ref(false);
const error = ref('');

const loginForm = reactive({
  username: '',
  password: '',
});

const rules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
});

const submitForm = async () => {
  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      error.value = '';
      try {
        // The backend expects 'application/x-www-form-urlencoded' for the OAuth2 form
        const formData = new URLSearchParams();
        formData.append('username', loginForm.username);
        formData.append('password', loginForm.password);
        await authStore.login(formData);
      } catch (err) {
        error.value = '登录失败，请检查您的用户名和密码。';
        console.error(err);
      } finally {
        loading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.card-header {
  text-align: center;
}
.error-alert {
  margin-top: 20px;
}
</style>
