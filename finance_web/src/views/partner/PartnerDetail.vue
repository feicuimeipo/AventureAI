<template>
  <!-- ═══ VIEW: DETAIL ═══ -->
  <div class="view" id="view-detail">
    <div class="detail-wrap">
      <div class="back-btn" @click="router.go(-1)">← 返回列表</div>
      <div v-if="message.length > 1" style="padding-left: 5px">{{ message }}</div>
      <div class="detail-card" v-else>
        <!-- Hero -->
        <div class="detail-hero">
          <div
            class="d-avatar"
            style="
              background: #e6f4f1;
              color: var(--teal);
              width: 80px;
              height: 80px;
              font-size: 36px;
            "
          >
            {{ candidate.firstName }}
          </div>
          <div class="d-info">
            <div class="d-name">{{ candidate.displayName }}</div>
            <div class="d-role">{{ getRoleDesc(candidate.role) }}</div>
            <div class="d-meta">
              <span class="d-meta-item">📈 {{ candidate.needTags }}</span>
              <span class="d-meta-item">🚀 {{ candidate.industryTags }}</span>
              <span class="d-meta-item" v-if="candidate.candidateRole == 'founder'"
                >🛡️ {{ candidate.projectName }} - {{ candidate.projectStage }} -
                {{ candidate.fundingStage }}
              </span>
              <span class="d-meta-item" v-if="candidate.candidateRole == 'investor'"
                >💰 {{ candidate.investmentTags }}
              </span>
              <span
                class="d-meta-item"
                v-if="candidate.candidateRole == 'expert' || candidate.candidateRole == 'fa'"
                >📊 {{ candidate.workType }}
              </span>
              <span class="d-meta-item">📍 {{ candidate.city }}</span>
              <span class="d-meta-item">🕐 {{ candidate.lastActiveTimeDesc }}</span>
            </div>
            <div class="d-bio">
              {{ candidate.bio }}
            </div>
          </div>
          <div class="d-score-wrap">
            <div class="d-score-big">{{ candidate.scoreTotal }}</div>
            <div class="d-score-sub">MATCH SCORE</div>
            <div style="margin-top: 12px; font-size: 11px; color: var(--muted)">
              {{ candidate.featureDesc }}
            </div>
          </div>
        </div>

        <!-- Match Analysis -->
        <div class="detail-section">
          <div class="ds-title">MATCH ANALYSIS·匹配分析</div>
          <PartnerCandidateRadarChart :matchResultId="matchResultId" />
          <!-- AI Reason -->
          <div
            style="
              margin-top: 20px;
              padding: 16px;
              border-radius: 8px;
              border-left: 3px solid var(--teal);
            "
          >
            <div
              style="
                font-size: 11px;
                color: var(--teal);
                letter-spacing: 0.08em;
                margin-bottom: 6px;
              "
            >
              AI 推荐理由
            </div>
            <div style="font-size: 13px; color: var(--ink2); line-height: 1.8">
              <span v-for="(v, index) in candidate.reasons" :key="index"> {{ v }} <br /> </span>
            </div>
          </div>

          <!-- 技能 -->
          <div
            style="
              margin-top: 20px;
              padding: 16px;
              border-radius: 8px;
              border-left: 3px solid var(--teal);
            "
          >
            <div
              style="
                font-size: 11px;
                color: var(--teal);
                letter-spacing: 0.08em;
                margin-bottom: 6px;
              "
            >
              技术标签
            </div>
            <div style="font-size: 13px; color: var(--ink2); line-height: 1.8">
              <span v-for="(v, index) in candidate.skillTags" :key="index"> {{ v }} <br /> </span>
            </div>
          </div>
        </div>

        <!-- Experience -->
        <div class="detail-section">
          <div class="ds-title">EXPERIENCE·经历</div>
          <div class="exp-timeline">
            这家伙很懒，没写经历
            <!--            <div class="exp-item">-->
            <!--              <div-->
            <!--                style="-->
            <!--                  display: flex;-->
            <!--                  flex-direction: column;-->
            <!--                  align-items: center;-->
            <!--                  gap: 0;-->
            <!--                  width: 10px;-->
            <!--                  flex-shrink: 0;-->
            <!--                  margin-top: 4px;-->
            <!--                "-->
            <!--              >-->
            <!--                <div class="exp-dot"></div>-->
            <!--                <div style="width: 2px; flex: 1; background: var(&#45;&#45;border); min-height: 40px"></div>-->
            <!--              </div>-->
            <!--              <div class="exp-body" style="padding-bottom: 16px">-->
            <!--                <div class="exp-title">高级后端工程师 → 技术 Lead</div>-->
            <!--                <div class="exp-company">字节跳动 · 飞书事业部</div>-->
            <!--                <div class="exp-period">2019.06 — 2024.03 · 5年</div>-->
            <!--              </div>-->
            <!--            </div>-->
            <!--            <div class="exp-item">-->
            <!--              <div-->
            <!--                style="-->
            <!--                  display: flex;-->
            <!--                  flex-direction: column;-->
            <!--                  align-items: center;-->
            <!--                  gap: 0;-->
            <!--                  width: 10px;-->
            <!--                  flex-shrink: 0;-->
            <!--                  margin-top: 4px;-->
            <!--                "-->
            <!--              >-->
            <!--                <div class="exp-dot"></div>-->
            <!--                <div style="width: 2px; flex: 1; background: var(&#45;&#45;border); min-height: 40px"></div>-->
            <!--              </div>-->
            <!--              <div class="exp-body" style="padding-bottom: 16px">-->
            <!--                <div class="exp-title">全栈工程师</div>-->
            <!--                <div class="exp-company">Meituan · 技术中台</div>-->
            <!--                <div class="exp-period">2017.07 — 2019.05 · 2年</div>-->
            <!--              </div>-->
            <!--            </div>-->
            <!--            <div class="exp-item">-->
            <!--              <div style="width: 10px; flex-shrink: 0; margin-top: 4px">-->
            <!--                <div class="exp-dot"></div>-->
            <!--              </div>-->
            <!--              <div class="exp-body">-->
            <!--                <div class="exp-title">计算机科学与技术 · 本科</div>-->
            <!--                <div class="exp-company">同济大学</div>-->
            <!--                <div class="exp-period">2013 — 2017</div>-->
            <!--              </div>-->
            <!--            </div>-->
          </div>
        </div>

        <!-- Send Interest -->
        <div class="detail-section">
          <div class="ds-title">CONNECT · 发起连接</div>
          <div class="msg-panel">
            <div class="msg-title">向{{ candidate.displayName }} 表达合作兴趣</div>
            <div class="msg-note">
              双方互相表达兴趣后，私信功能将解锁。请简单介绍你的项目和希望合作的方式。
            </div>
            <textarea
              class="msg-input"
              id="interestMessage"
              v-model="interestMessage"
              :placeholder="`你好，我在做一个 ${candidate.industryReq} 方向的项目，看到你的背景非常匹配，希望有机会聊聊……`"
            ></textarea>
            <!--            <div style="font-size: 12px">-->
            <!--              <label for="interactionType">意向 &nbsp;&nbsp;</label>-->
            <!--              <span v-for="(item, index) in InteractionTypeList" :key="index">-->
            <!--                <input-->
            <!--                  type="radio"-->
            <!--                  id="interactionType"-->
            <!--                  :value="item.tag"-->
            <!--                  v-model="interactionType"-->
            <!--                />{{ item.name }}&nbsp;&nbsp;-->
            <!--              </span>-->
            <!--            </div>-->

            <div class="msg-actions">
              <button
                class="btn-send-msg"
                @click="expressInteraction('interest')"
                v-if="!candidate.isInterest"
              >
                💚 表达兴趣
              </button>
              <button class="btn-interest saved" v-else disabled style="color: var(--teal)">
                ✓ 已表达兴趣,等待回应
              </button>

              <button
                class="btn-save"
                @click="expressInteraction('favorite')"
                v-if="!candidate.isFavorite"
              >
                直接收藏
              </button>
              <button class="btn-save saved" v-else @click="cancelFavorite">
                ✓已收藏，点击取消收藏
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { ref, onMounted, reactive } from 'vue';
import { addAction, cancelAction, getCandidateDetail } from '@/api/need/partner.ts';
import PartnerCandidateRadarChart from '@/components/PartnerCandidateRadarChart.vue';
import MessageBox from '@/utils/MessageBox.ts';
import { getRoleDesc } from '@/utils/userData.ts';
const router = useRouter();
const route = useRoute();
const candidate = reactive<any>({});
const interestMessage = ref<string>('');
const matchResultId = route.params.id.toString();
const message = ref<string>('');
onMounted(() => {
  if (matchResultId == ':id') {
    message.value = '请选择一个搭子';
  } else {
    message.value = '';
    getCandidateDetail(matchResultId)
      .then((res: any) => {
        if (res.code == 0) {
          Object.assign(candidate, res.data);
          if (candidate.displayName && candidate.displayName.length >= 1) {
            candidate['firstName'] = candidate.displayName.substring(0, 1);
          }
          interestMessage.value =
            '你好，我在做一个 ' +
            candidate.industryReq +
            ' 方向的项目，看到你的背景非常匹配，希望有机会聊聊……';
        } else {
          message.value = '请选择一个搭子';
        }
      })
      .catch(err => {
        console.log(err);
      });
  }
});

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

const cancelFavorite = () => {
  const param = {
    from_user_id: candidate.seekerId,
    to_user_id: candidate.candidateId,
    result_id: candidate.id,
    action: 'favorite',
  };
  cancelAction(param).then((res: any) => {
    if (res.code == 0) {
      candidate.isFavorite.value = false;
    }
  });
};
</script>

<style scoped lang="scss"></style>
