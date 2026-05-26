<template>
  <div :class="moduleStyle">
    <div class="flex gap-2">
      <div v-if="isLoggedIn == false" class="user-login-register">
        <BtnRegisterLogin
          :display-login-btn="displayLoginBtn"
          :display-register-btn="displayRegisterBtn"
        />
      </div>
      <div class=" user-login-register" v-if="isLoggedIn">
        <a @click="doLogout" class="logout" style="cursor: pointer">登出</a>
      </div>

      <div class="hidden md:flex gap-2 m-2 nav-token" v-if="isLoggedIn">
        <div class="token-icon" style="font-size: 12px">Token</div>
        <div>
          <div class="token-label" id="navBalance">总额：1,840</div>
          <div class="token-label" id="navChange">今日：+40</div>
        </div>
      </div>
      <div class="hidden md:flex user-chip" v-if="isLoggedIn">
        <div class="user-avatar">{{ firstName }}</div>
        <div class="user-name">{{ displayName }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import '@/styles/module-user-state.scss';
import {  onMounted, ref } from 'vue';
import BtnRegisterLogin from '@/components/BtnRegisterLogin.vue';
import { useCurrentUserStore } from '@/stores/currentUser.ts';
import {  useRouter } from 'vue-router';

const props = withDefaults(
  defineProps<{
    cssmodule?: string;
    displayLoginBtn?: boolean;
    displayRegisterBtn?: boolean;
  }>(),
  {
    cssmodule: 'module-default',
    displayLoginBtn: true,
    displayRegisterBtn: true,
  }
);
const currentUser = useCurrentUserStore();
const firstName = ref<string>('');
const displayName = ref<string>('');
const isLoggedIn = ref<boolean>(currentUser.isLogin);

const router = useRouter();
const getUserInfo = async () => {
  currentUser
    .fetchCurrentUserInfo()
    .then(() => {
      displayName.value = currentUser.getUserInfo().displayName;
      firstName.value = currentUser.getUserInfo().firstName;
    })
    .catch(err => {
      console.log(err);
    });
};

// const route = useRoute();
onMounted(() => {
  currentUser.loginState().then(() => {
    isLoggedIn.value = currentUser.isLogin;
    console.log('current_login-status:' + currentUser.isLogin);
    if (currentUser.isLogin) {
      getUserInfo();
    }
  });
  console.log('isLoggedIn=' + isLoggedIn.value);
});

const moduleStyle = ref<string>(props.cssmodule ? props.cssmodule : 'module-default');

const doLogout = () => {
  try {
    useCurrentUserStore().logout();
    router.push('/login');
  } catch (err) {
    console.error(err);
  }
};
</script>

<style scoped lang="scss"></style>
