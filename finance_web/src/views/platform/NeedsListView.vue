<template>
  <div :class="moduleStyle">
    需求列表
  </div>
</template>

<script setup lang="ts">
  import {getNeedsStyleClass} from "@/utils/menuUtils.ts";

  const moduleStyle = getNeedsStyleClass();
</script>

<style scoped>

</style>
