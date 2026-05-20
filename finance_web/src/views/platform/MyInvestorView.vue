<template>
  <div class="screen">
    <div class="cf-layout">
      <div class="cf-sidebar">
        <MyCandidateListView type="investor" />
      </div>
      <div class="cf-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MyCandidateListView from '@/views/platform/common/MyCandidateListView.vue';
</script>

<style scoped lang="scss"></style>
