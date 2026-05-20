<template>
  <div class="panel-title">注册流程</div>
  <div class="panel-sub">完成4步设置，开始你的创投生态之旅</div>
  <div class="steps" id="stepList">
    <div v-for="item in stepList" :key="item.num">
      <div v-if="active_step_num == item.num" class="step active">
        <div class="step-num">{{ item.num }}</div>
        <div class="step-info">
          <div class="step-name">{{ item.name }}</div>
          <div class="step-desc">{{ item.desc }}</div>
        </div>
      </div>
      <div v-else class="step">
        <div class="step-num">{{ item.num }}</div>
        <div class="step-info">
          <div class="step-name">{{ item.name }}</div>
          <div class="step-desc">{{ item.desc }}</div>
        </div>
      </div>
      <div v-if="item.num != 4" class="connector"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
const route = useRoute();

const getActiveStepNum = (path: string) => {
  if (path.endsWith('/register')) {
    active_step_num.value = 1;
  } else if (path.endsWith('/role')) {
    active_step_num.value = 2;
  } else if (path.endsWith('/profile')) {
    active_step_num.value = 3;
  } else if (path.endsWith('/finish')) {
    active_step_num.value = 4;
  }
};

const active_step_num = ref<number>(1);
getActiveStepNum(route.path);
watch(route, () => {
  getActiveStepNum(route.path);
});

interface Steps {
  name: string;
  desc: string;
  num: number;
}

const stepList: Steps[] = [
  {
    name: '基本信息',
    desc: '手机号或邮箱 + 密码',
    num: 1,
  },
  {
    name: '选择角色',
    desc: '告诉我们你的身份定位',
    num: 2,
  },
  {
    name: '完善档案',
    desc: '个性化信息，提升匹配质量',
    num: 3,
  },
  {
    name: '开始使用',
    desc: '领取100 Token 奖励',
    num: 4,
  },
];
</script>

<style scoped>
.panel-sub {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.7;
  margin-bottom: 40px;
}

.panel-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.step.active {
  background: var(--gold-dim);
  border-color: var(--gold-glow);
}

.step.active .step-num {
  border-color: var(--gold);
  background: var(--gold);
  color: #000;
  font-weight: 700;
}
.step.active .step-name {
  color: var(--gold);
}

.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1.5px solid var(--muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Mono', monospace;
  font-size: var(--font-size-base);
  color: var(--muted);
  flex-shrink: 0;
  transition: all 0.2s;
}

.step-name {
  font-size: var(--font-size-14);
  font-weight: 500;
  margin-bottom: 3px;
}

.step-desc {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.5;
}

.connector {
  width: 1.5px;
  height: 24px;
  background: var(--muted);
  margin-left: 29px;
}
</style>
