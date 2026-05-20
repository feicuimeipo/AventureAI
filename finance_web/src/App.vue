<template>
  <BApp>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </BApp>
</template>

<style scoped></style>
<script setup lang="ts">
import { BApp } from 'bootstrap-vue-next';
</script>
