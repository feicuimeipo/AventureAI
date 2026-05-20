<template>
  <button :style="fontStyle" class="btn" @click="navigateTo(path)" :id="id">
    {{ label }}
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { defineProps } from 'vue';

withDefaults(
  defineProps<{ id: string; label: string; fontStyle: string,path:string }>(),
  {
    id: '',
    label: '',
    fontStyle: '',
    path: '',
  }
);

const router = useRouter();
const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<style scoped lang="scss">
.btn {
  font-size: var(--font-size-base);
  letter-spacing: 0.12em;
  padding: 5px 14px;
  border-radius: 2px;
  cursor: pointer !important;
  transition: all 0.2s;
}

.module-platform,
.module-login-register,
.module-default {
  .btn {
    color: var(--gold);
    background: var(--gold-dim);
    border: 1px solid var(--gold-line);
  }
}

.module-newsfeed {
  .btn {
    color: var(--ink);
    background: var(--white);
    border: 1px solid var(--ink);
  }
}

.module-token {
  .btn {
    color: var(--gold);
    background: var(--gold-dim);
    border: 1px solid var(--gold-line);
  }
}
</style>
