<template>
  <!-- ═══ VIEW: DISCOVER ═══ -->
  <div id="view-discover">
    <div class="discover-header">
      <div>
        <div class="discover-title">匹配搭子</div>
        <!--        <div class="discover-sub flex gap-2">-->
        <!--          基于你的档案和需求，AI为你精选了-->
        <!--          <strong style="color: var(&#45;&#45;teal)">{{ total }}</strong> 位高匹配候选人-->
        <!--        </div>-->
      </div>
      <div class="discover-order-box">
        <div class="md:hidden flex items-center">
          <select
            class="discover-order-by"
            @change="switchOrderType"
            id="currentNeedId"
            v-model="currentNeedId"
          >
            <option
              v-for="(item, index) in needs"
              :key="index"
              :value="item.id"
              @change="handleSearch"
            >
              {{ item.title }}
            </option>
          </select>
        </div>

        <select class="discover-order-by" @change="switchOrderType" v-model="selectedOrderBy">
          <option value="score" selected>按匹配度排序</option>
          <option value="lastActive">按最近活跃</option>
          <option value="registerTime">按最新加入</option>
        </select>
        <!--        <div class="view-toggle">-->
        <!--          <div class="vt-btn on" title="卡片视图">▦</div>-->
        <!--          <div class="vt-btn" title="列表视图">☰</div>-->
        <!--        </div>-->
      </div>
    </div>
    <!-- style="animation: fadeUp 0.3s ease 0.05s both" -->
    <div class="cards-grid">
      <div
        v-for="(item, index) in dataList"
        :key="index"
        @click="navigatorToDetail(item.id)"
        :class="item.feature"
      >
        <div class="score-bar">
          <div class="score-fill score-high" :style="{ width: `${item.scoreTotal}%` }"></div>
        </div>
        <div class="card-body">
          <div class="card-head">
            <div class="avatar-wrap">
              <div class="c-avatar" style="background: #e6f4f1; color: var(--teal)">
                {{ item.displayName.substring(0, 1) }}
              </div>
              <div class="online-dot"></div>
            </div>
            <div class="card-info">
              <div class="card-name">{{ item.displayName }}</div>
              <div class="card-role">{{ item.role }} · {{ item.title }} · {{ item.city }}</div>
            </div>
            <div class="match-score-badge score-badge-high">
              <div class="score-num">{{ item.scoreTotal }}</div>
              <div class="score-label">MATCH</div>
            </div>
          </div>
          <div class="card-bio">{{ item.bio }}</div>
          <div class="match-reasons">
            <div class="match-reasons-label">AI MATCH REASONS</div>
            <div class="reason-chips">
              <div v-for="(v, i) in item.reasons" :key="i">
                <span class="reason-chip reason-skill">{{ v }}</span>
              </div>
            </div>
          </div>
          <div class="skill-tags">
            <div v-for="(v, i) in item.skillTags" :key="i">
              <span class="skill-tag match">{{ v }}}</span>
            </div>
          </div>
          <div class="card-footer">
            <button
              class="btn-interest"
              @click="navigatorToDetail(item.id)"
              v-if="!item.isInterest"
            >
              💚 表达兴趣
            </button>
            <span v-else>✓ 已表达兴趣,等待回应</span>
            <!--            <select :id="`interactionType_${item.id}`">-->
            <!--              <option value="" disabled>请选择收藏类型</option>-->
            <!--              <option v-for="(item, index) in InteractionTypeList" :value="item.tag" :key="index">-->
            <!--                {{ item.name }}-->
            <!--              </option>-->
            <!--            </select>-->
            <button
              class="btn-save"
              @click="addFavorite(item.id, item.need_id, item.seeker_id, item.candidate_id)"
              v-if="!item.isFavorite"
              title="收藏"
              :id="`btn_favorite_${item.id}`"
            >
              🔖
            </button>
            <button class="btn-save saved" v-else disabled title="已收藏">√已收藏</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!dataList || dataList.length <= 0" style="padding: 20px">{{ dataListMessage }}</div>
    <div class="load-more">
      <button class="btn-load" v-if="hasMore" @click="goNextPage">
        {{ loading ? '加载中...' : '点击加载更多' }}
      </button>
      <span class="load-bottom" v-else> ---到底了--- </span>
      <div style="font-size: 11px; color: var(--muted); margin-top: 12px">
        已显示 {{ displayCount }} / {{ total }} · 匹配度 ≥ {{ queryParam.rangeValue }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// import '@/styles/module_partner.scss';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, reactive, ref } from 'vue';
import { addAction, findMatchResultByParams } from '@/api/need/partner.ts';
import { userQueryParam } from '@/hooks/userQueryParam.ts';
import MessageBox from '@/utils/MessageBox.ts';
import type { NeedVO, PartnerSearchDTO } from '@/types/needBO.ts';
import { getNeedList } from '@/api/need/need.ts';

const router = useRouter();
const navigatorToDetail = (id: any) => {
  router.push({
    name: 'partner_detail',
    params: { id },
  });
};

const route = useRoute();
const dataList = reactive<any[]>([]);
const page = ref<number>(1);
const perPage = ref<number>(10);
const total = ref<number>(0);
const displayCount = ref<number>(0);
const hasMore = ref<boolean>(true);
const loading = ref(false);
const dataListMessage = ref<string>();
const selectedOrderBy = ref<string>('score');
// const InteractionTypeList = reactive(InteractionTypesItems);
const queryParam = reactive<PartnerSearchDTO>({} as PartnerSearchDTO);

onMounted(() => {
  const { getStr, getNum } = userQueryParam();
  if (route.query) {
    const query = route.query;
    queryParam.needId = getStr(query.needId || '');
    // queryParam.roleWanted = getStr(query.roleWanted);
    // queryParam.workType = getStr(query.workType);
    // queryParam.industry = getStr(query.industry);
    // queryParam.cityReqs = getStr(query.cityReqs);
    // queryParam.skillReqs = getStr(query.skillReqs);
    queryParam.rangeValue = getNum(query.rangeValue) || 75;
  }

  page.value = 0;
  goNextPage();
  fetchNeeds();
});

const goNextPage = () => {
  loading.value = true;
  page.value = page.value + 1;
  const params = {
    ...queryParam,
    page: page.value,
    perPage: perPage.value,
  };

  findMatchResultByParams(params)
    .then((res: any) => {
      loading.value = false;
      if (res.code === 0) {
        Object.assign(dataList, res.data.list);
        page.value = res.data.page;
        perPage.value = res.data.perPage;

        hasMore.value = (dataList && dataList.length <= 0) || !dataList;

        total.value = res.data.total;
        displayCount.value = (page.value - 1) * perPage.value + res.data.list.length;
      } else {
        dataListMessage.value = res.message;
        hasMore.value = false;
      }
    })
    .catch(err => {
      loading.value = false;
      console.log(err);
    });
};

const addFavorite = (
  result_id: string,
  need_id: string,
  from_user_id: string,
  to_user_id: string
) => {
  const param = {
    from_user_id: from_user_id,
    to_user_id: to_user_id,
    result_id: result_id,
    need_id: need_id,
    action: 'favorite',
    interactionType: '-',
  };
  addAction(param).then((res: any) => {
    if (res.code === 0) {
      const btnFavorite = document.getElementById('btn_favorite_' + result_id);
      if (btnFavorite) {
        btnFavorite.setAttribute('disabled', 'true');
        btnFavorite.textContent = '√已收藏';
      }
    } else {
      MessageBox.Error(res.message);
    }
  });
};

const switchOrderType = () => {
  const params = {
    ...queryParam,
    orderBy: selectedOrderBy.value,
    page: 1,
    perPage: perPage.value,
  };

  findMatchResultByParams(params)
    .then((res: any) => {
      if (res.code === 0) {
        // Object.assign(dataList, res.data.list);
        const list = res.data.page;
        for (let i = 1; i < list.length; i++) {
          dataList.push(list[i]);
        }

        page.value = res.data.page;
        perPage.value = res.data.perPage;
        total.value = res.data.total;
        displayCount.value = (page.value - 1) * perPage.value + res.data.list.length;
      } else if (res.code == 404) {
        dataListMessage.value = '请选择一个搭子需求';
      } else if (res.code == 405) {
        dataListMessage.value = '请选择一个搭子需求';
      }
    })
    .catch(err => {
      console.log(err);
    });
};

// 获得需求列表
const needs = ref<NeedVO[]>([]);
const currentNeedId = ref<string>();
const fetchNeeds = async () => {
  getNeedList()
    .then((res: any) => {
      if (res.code == 0) {
        console.log('res.code:' + res.data.length);
        needs.value = res.data.map((row: any) => ({
          id: row.id,
          title: row.title,
          roleWanted: row.role_wanted,
          workType: row.work_type,
          skillReq: row.skill_req,
          industry: row.industry,
          cityReq: row.city_req,
        })) as NeedVO[];
        if (needs.value.length > 0) {
          currentNeedId.value = needs.value[0].id;
          handleSearch();
        }
      }
    })
    .catch(err => {
      console.log('获取需求列表失败:', err);
    });
};

const handleSearch = () => {
  const searchParam = {
    needId: currentNeedId.value,
    rangeValue: 50,
  };

  router.push({
    name: 'partner_discovery',
    query: { ...searchParam },
  });
};
</script>

<style scoped lang="scss"></style>
