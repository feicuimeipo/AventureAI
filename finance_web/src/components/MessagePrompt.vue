<script setup lang="ts">
import { onMounted } from 'vue';

const props = withDefaults(
  defineProps<{
    id: string;
    color?: string;
  }>(),
  { id: 'liveAlertModal', color: 'red' }
);

// <div class="p-6 text-gray-700 leading-relaxed" :id="`${id}content`"> </div>

function openAlert(message: string) {
  const e = document.getElementById(props.id + 'content');
  if (e) e.textContent = message;
  const modal = document.getElementById(props.id);
  modal?.classList.remove('hidden');
}

function closeAlert() {
  const e = document.getElementById(props.id + 'content');
  if (e) e.textContent = '';
  const modal = document.getElementById(props.id);
  modal?.classList.add('hidden');
}

function confirmAction() {
  closeAlert();
}

//appendAlert(message, type, title, extra);
defineExpose({
  openAlert,
});

onMounted(() => {
  // 用户点击背景关闭弹窗
  const modal = document.getElementById(props.id);
  window.onclick = function (event) {
    if (event.target === modal) {
      closeAlert();
    }
  };
});
</script>

<template>
  <!-- 弹窗容器 -->
  <div
    :id="id"
    class="fixed inset-0 hidden z-50 backdrop-blur-sm bg-black bg-opacity-40 flex items-center justify-center px-4"
  >
    <div
      class="relative bg-white rounded-xl shadow-2xl overflow-hidden w-full max-w-sm animate-fadeInUp"
    >
      <!-- 头部 -->
      <div
        class="flex justify-between items-center border-b p-6 bg-gradient-to-r from-cyan-500 to-blue-500 text-white"
        style="padding: 4px;">
        <h3 class="text-sm font-semibold"><i class="fas fa-info-circle mr-2"></i>系统通知</h3>
        <button @click="closeAlert()" class="text-white hover:text-gray-200" style="font-size:20px;cursor:pointer;padding-right:5px">x</button>
      </div>

      <!-- 内容区 -->
      <div
        class="p-6 text-gray-700 leading-relaxed"
        style="padding: 5px"
        :id="`${id}content`"
      ></div>

      <!-- 底部按钮 -->
      <div class="border-t p-4 flex justify-end gap-x-3" style="padding: 5px">
        <button
          @click="confirmAction()"
          class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md shadow transition-transform duration-200 active:scale-95"
          style="padding: 5px;cursor:pointer"
        >
          确认
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>