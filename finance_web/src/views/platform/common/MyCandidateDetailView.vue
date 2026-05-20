<template>
  <div>
    <div style="font-size: 12px; margin-bottom: 16px">候选人详细 · AI推荐</div>
    <div class="cf-profile">
      <div class="cfp-top">
        <div class="cfp-av" style="background: #1a2a3a; color: #63b3ed">
          {{ candidate.firstName }}
        </div>
        <div class="cfp-info">
          <div class="cfp-name">{{ candidate.displayName }}</div>
          <div class="cfp-title">
            {{ getRoleDesc(candidate.role) }} · {{ candidate.title }} · {{ candidate.city }}
          </div>
        </div>
        <div class="cfp-match">
          <div class="cfp-match-n">{{ candidate.scoreTotal }}4%</div>
          <div class="cfp-match-l">综合匹配分</div>
        </div>
      </div>
      <div class="cfp-why">
        <strong>AI推荐理由：</strong>
        <span v-for="(v, index) in candidate.reasons" :key="index"> {{ v }} <br /> </span>
      </div>
      <div class="detail-section">
        <div class="ds-title">MATCH ANALYSIS　·　匹配分析</div>
        <PartnerCandidateRadarChart :matchResultId="matchResultId" />
      </div>
      <div class="pitch-gen-box">
        <div class="pgb-head">发送链接请求 - AI 破冰话术生成器</div>
        <div class="pgb-body">
          <div class="pgb-output live">
            <input
              type="text"
              class="field-input"
              style="background: #eeee; margin-bottom: 10px"
              id="interestMessageHeader"
              v-model="interestMessageHeader"
            />
            <textarea
              class="field-input"
              rows="5"
              style="background: #eeee"
              id="interestMessage"
              v-model="interestMessage"
            ></textarea>
          </div>
          <div class="pgb-actions">
            <div v-if="!candidate.isInterest" class="flex gap-2">
              <button class="pgb-btn pgb-primary" @click="expressInteraction('interest')">
                {{ interestBtnContent }}
              </button>
              <button class="pgb-btn pgb-sec" @click="regenPitch()">重新生成</button>
              <button class="pgb-btn pgb-sec" @click="copyMessage">复制</button>
            </div>
            <div v-else>
              <button class="pgb-btn pgb-primary" disabled>
                {{ interestBtnContent }} - 已发送
              </button>
              <button class="pgb-btn pgb-sec" disabled>重新生成</button>
              <button class="pgb-btn pgb-sec" disabled>复制</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="action-row primary">
      <button class="act-btn act-sec" @click="onViewDeepReport('深度报告')">深度报告</button>

      <button
        class="act-btn act-sec"
        @click="expressInteraction('favorite')"
        v-if="!candidate.isFavorite"
      >
        收藏
      </button>
      <button class="act-btn act-sec" @click="onViewDeepReport('深度报告')" v-else>已收藏</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { addAction, getCandidateDetail } from '@/api/need/partner.ts';
import MessageBox from '@/utils/MessageBox.ts';
import PartnerCandidateRadarChart from '@/components/PartnerCandidateRadarChart.vue';
import { useRoute } from 'vue-router';
import { getRoleDesc } from '@/utils/userData.ts';

const route = useRoute();
const candidate = reactive<any>({});

const interestMessageHeader = ref<string>('主题：关于AI知识管理——一个可能帮助美团工程效率的方向');

const interestMessage = ref<string>(
  '李总您好，\n' +
    '\n' +
    '    我是智链科技创始人张明远。通过您在QCon的演讲了解到，美团工程师平均每周花2.8小时查找内部文档——这正是我们解决的核心问题。\n' +
    '智链已帮助15家科技公司将知识检索效率提升3.2倍，对美团工程团队规模，月均可节省效率价值80-120万元。\n' +
    '愿意提供30天无风险POC，让数据说话。 请问下周是否有20分钟？\n' +
    '              '
);
const interestBtnContent = ref<string>('📧 发送连接请求');

const matchResultId = route.params.id.toString();

const regenPitch = () => {};

const copyMessage = () => {};
onMounted(() => {
  getCandidateDetail(matchResultId)
    .then((res: any) => {
      if (res.code == 0) {
        Object.assign(candidate, res.data);
        if (candidate.displayName && candidate.displayName.length >= 1) {
          candidate['firstName'] = candidate.displayName.substring(0, 1);
        }
      }
    })
    .catch(err => {
      console.log(err);
    });
});

const onViewDeepReport = (type: string) => {
  console.log(type);
};

const expressInteraction = (action: string) => {
  // if (!interactionType.value || interactionType.value == '') {
  //   MessageBox.Error('请选择兴趣或收藏意向');
  //   return;
  // }
  const param = {
    from_user_id: candidate.seekerId,
    to_user_id: candidate.candidateId,
    result_id: candidate.id,
    need_id: candidate.needId,
    message: interestMessage || '',
    action: action,
    interactionType: '-',
  };
  addAction(param).then((res: any) => {
    if (res.code == 0) {
      if (action == 'interest') {
        candidate.isInterest = true;
      } else if (action == 'favorite') {
        candidate.isFavorite = true;
      }
    } else {
      MessageBox.Error(res.message);
    }
  });
};
</script>

<style scoped lang="scss"></style>
