<template>
  <div class="radar-wrap flex">
    <v-chart class="chart" :option="radarChartOptions" autoresize />
    <v-chart class="chart" :option="barChartOptions" autoresize />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { RadarChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

import { GridComponent } from 'echarts/components';
import { BarChart } from 'echarts/charts';
import { getMatchScoreDetail } from '@/api/need/partner.ts';
import { useRoute } from 'vue-router';

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  //柱图添加的内容
  GridComponent,
  BarChart,
]);

// 定义默认值（可选）
// MatchScoreDetail
const props = defineProps<{
  matchResultId: string; // 注意：如果父组件必传，则不加 ?；如果可选，加 ? 并设置默认值
}>();
const radarChartOptions = ref({});
const barChartOptions = ref({});
const route = useRoute();
let matchResultId: string = route.params.id.toString();
onMounted(() => {
  if (props.matchResultId == undefined && matchResultId != null) {
    matchResultId = route.params.id.toString();
  }

  if (matchResultId != undefined) {
    getMatchScoreDetail(matchResultId).then((res: any) => {
      if (res.code == 0) {
        const scoreDetail = res.data;
        console.log(JSON.stringify('-----------' + JSON.stringify(scoreDetail)));

        const skill = scoreDetail.skill;
        const industry = scoreDetail.skill;
        const geo = scoreDetail.geo;
        const active = scoreDetail.active;
        const role = scoreDetail.role;

        radarChartOptions.value = {
          radar: {
            alignTicks: false,
            indicator: [
              { name: '技能', max: 100 },
              { name: '行业', max: 100 },
              { name: '城市', max: 100 },
              { name: '活跃', max: 100 },
              { name: '岗位', max: 100 },
            ],
            splitNumber: 4
          },
          series: [
            {
              type: "radar",
              data: [
                {
                  value: [skill, industry, geo, active, role],
                },
              ],
              itemStyle: {
                color: '#0f7b6c',
              },
            },
          ],
        };

        barChartOptions.value = {
          yAxis: {
            // type: 'category',
            data: ['技能匹配', '岗位互补', '活跃系数', '地理位置', '行业背景'],
            left: 'center',
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
          },
          xAxis: {
            type: 'value',
          },
          series: [
            {
              // name: '数据量',
              data: [skill, industry, geo, active, role],
              type: 'bar',
              itemStyle: {
                color: '#0f7b6c',
              },
            },
          ],
        };
      } else {
        //TODO： 。。。
      }
    });
  }
});
</script>

<style lang="scss">
/* 必须设置宽高，否则图表可能高度为0 */
.chart {
  width: 80%;
  height: 240px; /* 这里必须有一个具体的高度值 */
}
</style>