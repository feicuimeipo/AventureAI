<template>
  <span class="btn"> <a href="#" @click="goBack">返回上一页</a></span>
</template>

<style scoped>
.btn{
  font-size: var(--font-size-base);
  color: var(--muted);
}
</style>


<script setup lang="ts">
import {useRouter} from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}
</script>
