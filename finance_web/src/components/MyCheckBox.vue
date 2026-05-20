<script setup lang="ts">
import { ref } from 'vue';

defineProps<{ label: string }>();

const isChecked = ref<boolean>(false);
defineExpose({ isChecked });
</script>

<template>
  <label style="padding: 0;margin: 0">
    <input type="checkbox" :checked="isChecked" class="custom-checkbox" />
    <span class="checkbox-label" @click="isChecked=!isChecked">{{ label }}</span>
  </label>
</template>

<style scoped lang="scss">
.custom-checkbox {
  display: none;
}

/* 自定义复选框样式 */
.checkbox-label {
  position: relative;
  padding-left: 25px;
  cursor: pointer;
  user-select: none;
}

/* 创建自定义复选框外观 */
.checkbox-label::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  border: 2px solid #ccc;
  border-radius: 3px;
  background-color: white;
  transition: background-color 0.2s ease;
}

/* 选中时的背景颜色 */
.custom-checkbox:checked + .checkbox-label::before {
  background-color: var(--gold); /* 修改为你想要的背景色 */
  border-color: var(--gold);
}

/* 选中时添加对勾 */
.custom-checkbox:checked + .checkbox-label::after {
  content: '✓';
  position: absolute;
  left: 5px;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
}
</style>