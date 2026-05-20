<template>
  <div class="min-h-screen">
    <AppHeader subtitle="用户注册" :cssmodule="styleModule" />
    <div class="app flex">
      <div class="hidden md:ml-6 md:flex ">
        <div class="left">
          <UserRegisterRegisterGuide />
          <TokenAdvInfo />
        </div>
      </div>

      <div class="right">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import '@/styles/module-login-register.scss';
import TokenAdvInfo from '@/components/TokenAdvInfo.vue';
import AppHeader from '@/components/AppHeader.vue';
import { getDefaultModuleStyle } from '@/utils/menuUtils.ts';
import UserRegisterRegisterGuide from '@/views/users/register/UserRegisterRegisterGuide.vue';

const styleModule = getDefaultModuleStyle();
</script>

<style scoped></style>
