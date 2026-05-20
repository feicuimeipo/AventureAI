<template>
  <span class="login-register flex gap-1" ><a v-if="displayLoginBtn"  @click="navigateTo('/login')">{{ $t('login') }}</a>
    <span v-if="displayLoginBtn && displayRegisterBtn">/</span>
    <a  v-if="displayRegisterBtn" @click="navigateTo('/register')">{{ $t('register') }}</a>
  </span>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

defineProps<{
  displayLoginBtn?: boolean | true;
  displayRegisterBtn?: boolean | true;
}>();


const router = useRouter();
const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<style scoped lang="scss">
.login-register {
  font-size: var(--font-size-base);
}

.login-register a{
  cursor: pointer;
}


.module-partner {
  .login-register {
    color: var(--teal);
  }
}

.module-platform,
.module-login-register,
.module-default {
  .login-register {
    color: var(--muted);
  }
}

.module-newsfeed {
  .login-register {
    color: var(--ink);
  }
}

.module-token {
  .login-register {
    color: var(--gold);
  }
}
</style>
