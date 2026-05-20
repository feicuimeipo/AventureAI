<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { findMatchResultByParams } from '@/api/need/partner.ts';
import type { PartnerSearchDTO } from '@/types/needBO.ts';
import { useRoute, useRouter } from 'vue-router';

const dataList = reactive<any[]>([]);
const page = ref<number>(1);
const perPage = ref<number>(10);
const total = ref<number>(0);
const displayCount = ref<number>(0);
const hasMore = ref<boolean>(true);
const loading = ref(false);
const dataListMessage = ref<string>();
const queryParam = reactive<PartnerSearchDTO>({} as PartnerSearchDTO);

const props = defineProps<{
  type: string;
}>();

const route = useRoute();
onMounted(() => {
  queryParam.myCandidateType = props.type;
  if (props.type == undefined) {
    const paths = route.params.path.toString().split('/');
    queryParam.myCandidateType = paths[paths.length - 1];
  }

  page.value = 0;
  goNextPage();
});

const goNextPage = () => {
  loading.value = true;
  page.value = page.value + 1;
  const params = {
    myCandidateType: queryParam.myCandidateType,
    needId: '',
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

        hasMore.value = !res.data.isLastPage;

        total.value = res.data.total;
        displayCount.value = (page.value - 1) * perPage.value + res.data.list.length;
      } else if (res.code == 404) {
        dataListMessage.value = '请选择一个搭子需求';
      } else if (res.code == 405) {
        dataListMessage.value = '请选择一个搭子需求';
      } else {
        dataListMessage.value = res.message;
      }
    })
    .catch(err => {
      loading.value = false;
      console.log(err);
    });
};

const router = useRouter();
const navigatorToDetail = (id: string) => {
  let route_name = 'my_cofounder_detail';
  if (queryParam.myCandidateType == 'cofounder') {
    route_name = 'my_cofounder_detail';
  } else if (queryParam.myCandidateType == 'investor') {
    route_name = 'my_investor_detail';
  } else if (queryParam.myCandidateType == 'resource') {
    route_name = 'my_resource_detail';
  }
  router.push({
    name: route_name,
    params: {
      id: id
    },
  });
};
</script>

<template>
  <div class="cf-sb-head">AI推荐 · 高匹配候选人</div>
  <div
    class="cf-card on"
    v-for="(item, index) in dataList"
    :key="index"
    @click="navigatorToDetail(item.id)"
  >
    <div class="cf-card-top">
      <div class="cf-av" style="background: #1a2a3a; color: #63b3ed">
        {{ item.displayName.substring(0, 1) }}
      </div>
      <div>
        <div class="cf-name">{{ item.displayName }}</div>
        <div class="cf-title">{{ item.title }} · {{ item.city }}</div>
      </div>
      <div class="cf-score">{{ item.scoreTotal }}%</div>
    </div>
    <div class="cf-tags">
      <span
        class="cf-tag"
        style="background: rgba(99, 179, 237, 0.1); color: #63b3ed"
        v-for="v in item.skillTags"
        >{{ v }}</span
      >
    </div>
  </div>
  <div class="load-more">
    <br />
    <button class="btn-load" v-if="hasMore" @click="goNextPage">
      {{ loading ? '加载中...' : '点击加载更多' }}
    </button>
    <span class="load-bottom" v-else> ---到底了--- </span>
  </div>
</template>

<style scoped lang="scss"></style>