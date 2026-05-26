<template>
  <div class="section-panel" id="step3">
    <div class="success-panel">
      <div class="success-icon">🎉</div>
      <div class="success-title">恭喜您，注册成功！ <br/> 欢迎加入VentureAI！</div>
      <div class="form-actions" style="justify-content: center; margin-top: 32px">
        <button class="btn-primary" @click="toLoginPage">返回登录</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
const toLoginPage = () => {
  //业务处理
  router.push({
    path: '/login',
  });
};
</script>

<style scoped></style>
