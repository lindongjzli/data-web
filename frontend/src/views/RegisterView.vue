<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h2>创建新账户</h2>
      </div>
    </template>
    <el-form
      ref="registerFormRef"
      :model="registerForm"
      :rules="rules"
      label-width="80px"
      @submit.prevent="submitForm"
    >
      <el-form-item label="用户名" prop="username">
        <el-input v-model="registerForm.username"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registerForm.email"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="registerForm.password" show-password></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input type="password" v-model="registerForm.confirmPassword" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading">注册</el-button>
        <el-button @click="$router.push('/login')">已有账户？去登录</el-button>
      </el-form-item>
    </el-form>
    <el-alert v-if="error" :title="error" type="error" show-icon class="error-alert"></el-alert>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';

const authStore = useAuthStore();
const registerFormRef = ref<FormInstance>();
const loading = ref(false);
const error = ref('');

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else {
    if (registerForm.confirmPassword !== '') {
      if (!registerFormRef.value) return;
      registerFormRef.value.validateField('confirmPassword');
    }
    callback();
  }
};
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== registerForm.password) {
    callback(new Error("两次输入的密码不一致!"));
  } else {
    callback();
  }
};

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '长度应在 3 到 50 个字符之间', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] },
  ],
  password: [{ validator: validatePass, trigger: 'blur' }],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }],
});

const submitForm = async () => {
  if (!registerFormRef.value) return;
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      error.value = '';
      try {
        await authStore.register({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
        });
        ElMessage({
          message: '注册成功！将跳转到登录页面。',
          type: 'success',
        });
      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          error.value = `注册失败: ${err.response.data.detail}`;
        } else {
          error.value = '注册失败，请稍后重试。';
        }
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
