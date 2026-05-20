<template>
  <!-- My Need Card -->
  <div class="my-need">
    <div class="my-need-label">
      我的需求列表 &nbsp;<a class="edit-need" href="#" @click="onAddNeed()">发布需求</a>
    </div>
    <div v-for="(item, index) in needs" :key="index">
      <div class="my-need-title">
        <a class="view-need" href="#" @click="onViewDetail(item)" style="cursor: pointer"
          >{{ item.title }}
        </a>
        <a class="edit-need" href="#" @click="onEditNeed(item)">修改</a>
      </div>
    </div>
  </div>

  <div class="sidebar-section">
    <div class="sidebar-label flex">
      <span> {{ formData.title }}-筛选：</span>
    </div>
    <div class="filter-group">
      <div class="filter-title">角色类型</div>
      <div class="filter-tags">
        <div
          v-for="(item, index) in searchRoleWanted"
          :key="index"
          :class="item.class"
          @click="toggleFtag"
          :data-tag="item.tag"
          data-type="role"
        >
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="filter-group">
      <div class="filter-title">参与方式</div>
      <div class="filter-tags">
        <div
          v-for="(item, index) in searchTagWorkType"
          :key="index"
          :class="item.class"
          @click="toggleFtag"
          :data-tag="item.tag"
          data-type="workType"
        >
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="filter-group">
      <div class="filter-title">城市</div>
      <div class="filter-tags">
        <div
          v-for="(item, index) in searchTagCityType"
          :key="index"
          :class="item.class"
          @click="toggleFtag"
          :data-tag="item.tag"
          data-type="city"
        >
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="filter-group">
      <div class="filter-title">赛道偏好</div>
      <div class="filter-tags">
        <div
          v-for="(item, index) in industries"
          :key="index"
          :class="item.class == 't-chip' ? 'stag' : item.class"
          @click="toggleFtag"
          :data-tag="item.tag"
          data-type="industry"
        >
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="filter-group">
      <div class="filter-title">
        最低匹配分
        <span style="color: var(--teal)" id="rangeVal">{{ rangeVal }}</span>
      </div>
      <input type="range" min="50" max="99" value="75" @input="setRangeVal" />
      <div class="slider-labels"><span>50</span><span>99</span></div>
    </div>
  </div>
  <!--  <div style="flex: 1"></div>-->
  <!--  <div-->
  <!--    style="-->
  <!--      padding: 16px 20px;-->
  <!--      font-size: 11px;-->
  <!--      color: var(&#45;&#45;muted);-->
  <!--      line-height: 1.6;-->
  <!--      border-top: 1px solid var(&#45;&#45;border);-->
  <!--    "-->
  <!--  >-->
  <!--    <span style="color: var(&#45;&#45;teal); font-family: 'DM Mono', monospace">247</span>-->
  <!--    位搭子正在寻找合作 · 今日新增-->
  <!--    <span style="color: var(&#45;&#45;teal); font-family: 'DM Mono', monospace">12</span>-->
  <!--  </div>-->
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { getNeedList } from '@/api/need/need.ts';
import type { NeedVO } from '@/types/needBO.ts';
import { IndustryItems } from '@/utils/userData.ts';
import {
  ParticipationItems,
  SearchTagCities,
  SearchTagRoleWanted,
} from '@/utils/needData.ts';
import { useRouter } from 'vue-router';

const needs = ref<NeedVO[]>([]);
const searchRoleWanted = reactive(SearchTagRoleWanted);
const searchTagWorkType = reactive(ParticipationItems);
const searchTagCityType = reactive(SearchTagCities);
const industries = reactive(IndustryItems);
const formData = reactive<NeedVO>({
  id: '',
  title: '',
  roleWanted: '',
  workType: '',
  cityReqs: '',
  description: '',
  industry: '',
  skillReqs: '',
  equityRange: '',
} as NeedVO);

const fetchNeeds = async () => {
  const results: NeedVO[] = [];
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

        if (res.data.length > 0) {
          const need = res.data[0];
          formData.id = need.id;
          formData.title = need.title;
          formData.roleWanted = need.role_wanted;
          formData.workType = need.work_type;
          formData.skillReqs = need.skill_reqs;
          formData.industry = need.industry;
          formData.cityReqs = need.city_reqs;
          setDefaultSearchCondition(formData);
        }
      }
    })
    .catch(err => {
      console.log('获取需求列表失败:', err);
    });
  return results;
};

const setDefaultSearchCondition = (formData: any) => {
  const roleWanted = formData.roleWanted;
  const skillReq = formData.skillReq;

  searchRoleWanted.forEach((item: any) => {
    item.class = 'ftag';
    const ary = item.roleWanted.split(',');
    if (ary.includes(roleWanted)) {
      item.class = 'ftag on';
    }
    if (skillReq in item.skillReq.split(',')) {
      item.class = 'ftag on';
    }
  });

  searchTagWorkType.forEach((item: any) => {
    item.class = 'ftag';
    if (formData.workType == item.tag) {
      item.class = 'ftag on';
    }
  });

  const cities = ',' + formData.cityReqs + ',';

  searchTagCityType.forEach((item: any) => {
    item.class = 'ftag';
    if (cities.indexOf(',' + item.tag + ',') > -1) {
      for (let i = 0; i < formData.cityReqs.length; i++) {
        if (formData.cityReqs[i] == item.tag) {
          item.class = 'ftag on';
        }
      }
    }
  });

  industries.forEach((item: any) => {
    item.class = 'ftag';
    if (formData.industry == item.tag) {
      item.class = 'ftag on';
    }
  });
};

onMounted(() => {
  fetchNeeds();
});

const router = useRouter();
const emit = defineEmits(['handleNeed']);
const onViewDetail = (item: NeedVO) => {
  handleSearch(item.id);
  setDefaultSearchCondition(item);
};

const onAddNeed = () => {
  emit('handleNeed', 'add', null);
};

const onEditNeed = (item: NeedVO) => {
  emit('handleNeed', 'edit', item);
  onViewDetail(item);
};

const toggleFtag = (e: any) => {
  const event = e.currentTarget;

  if (event.dataset.type == 'city') {
    searchTagCityType.forEach((item: any) => {
      if (event.dataset.tag == item.tag) {
        if (item.class.indexOf('on') == -1) {
          item.class = 'ftag on';
        } else {
          item.class = 'ftag';
        }
      }
    });
  }

  if (event.dataset.type == 'workType') {
    // item.class = 'ftag';
    searchTagWorkType.forEach((item: any) => {
      if (event.dataset.tag == item.tag) {
        if (item.class.indexOf('on') == -1) {
          item.class = 'ftag on';
        } else {
          item.class = 'ftag';
        }
      }
    });
  }

  if (event.dataset.type == 'industry') {
    // item.class = 'ftag';
    industries.forEach((item: any) => {
      if (event.dataset.tag == item.tag) {
        if (item.class.indexOf('on') == -1) {
          item.class = 'ftag on';
        } else {
          item.class = 'ftag';
        }
      }
    });
  }

  if (event.dataset.type == 'role') {
    searchRoleWanted.forEach((item: any) => {
      if (event.dataset.tag == item.tag) {
        if (item.class.indexOf('on') == -1) {
          item.class = 'ftag on';
        } else {
          item.class = 'ftag';
        }
      }
    });
  }
};

const rangeVal = ref<number>(75);
const setRangeVal = (e: any) => {
  const o = e.currentTarget;
  rangeVal.value = o.value;
};

const handleSearch = (id: string) => {
  const searchParam = {
    needId: id,
    rangeValue: rangeVal.value,
  };

  router.push({
    name: 'partner_discovery',
    query: { ...searchParam },
  });
};
</script>

<style scoped lang="scss"></style>
