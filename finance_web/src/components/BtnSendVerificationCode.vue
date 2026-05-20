<script setup lang="ts">
import { reactive } from 'vue';

const emit = defineEmits(['sendVerificationCode']);

// 状态管理
const state = reactive({
  isSending: false,
  countdown: 60,
  timer: null as number | null,
});

// 开始倒计时
function startCountdown() {
  state.isSending = true;
  state.countdown = 60;
  state.timer = setInterval(() => {
    if (state.countdown > 0) {
      state.countdown--;
    } else {
      stopTimer();
    }
  }, 1000);
}

// 清除定时器
function stopTimer() {
  if (state.timer !== null) {
    clearInterval(state.timer);
    state.timer = null;
  }
  state.isSending = false;
}

// 触发发送验证码
async function handleSendCode() {
  try {
    // 通过emit触发事件并等待返回值
    // state.isSending = true;
    startCountdown();
    const resultValue = await new Promise(resolve => {
      emit('sendVerificationCode', resolve);
    });
    if (!resultValue) {
      stopTimer();
      // state.isSending = false;
    }
  } catch (error) {
    console.log(error);
    stopTimer();
  }
}
</script>

<template>
  <button
    type="button"
    class="btn-primary-reverse"
    id="sendBtn"
    @click="handleSendCode"
    :disabled="state.isSending"
  >
    {{ state.isSending ? `${state.countdown}s 后重试` : '获取验证码' }}
  </button>
</template>

<style scoped lang="scss">
.btn-primary-reverse:disabled {
  background-color: lightgray;
  cursor: default;
}
</style>
