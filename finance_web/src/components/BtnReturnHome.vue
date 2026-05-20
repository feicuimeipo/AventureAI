<template>
  <span class="return-home" @click="navigateTo('/')">
      <HomeIcon class="size-6 align-items-center justify-content-center text-center" />
  </span>
</template>

<script setup lang="ts">
import { HomeIcon } from '@heroicons/vue/24/solid';
import { useRouter } from 'vue-router/dist/vue-router.js';


const router = useRouter()
const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped lang="scss">

.return-home {
  font-size: var(--font-size-16);
  text-align: center;
  cursor: pointer;
}


.module-partner{
  .return-home{
    color: var(--teal);
  }
}

.module-platform,
.module-login-register,
.module-default{
  .return-home{
    color: var(--muted);
  }
}

.module-newsfeed{
  .return-home{
    color: var(--ink);
  }
}

.module-token{
  .return-home{
    color: var(--gold);
  }
}

</style>
