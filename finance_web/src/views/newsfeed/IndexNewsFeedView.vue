<template>
  <div :class="moduleStyle">
    <div class="min-h-screen">
      <div>
        <AppHeader subtitle="Intelligence" :cssmodule="moduleStyle" />

        <nav class="nav-bar">
          <div class="nav-item on" @click="toIndex()">全部</div>
          <div class="nav-sep"></div>
          <div v-for="(item, index) in menuList" :key="index">
            <div
              v-if="item.isHot"
              class="nav-item hot"
              :dataset-path="item.path"
              @click="toNewsList"
            >
              {{ item.icon }} {{ item.name }}
            </div>
            <div v-else class="nav-item" :dataset-path="item.path" @click="setNav">
              {{ item.icon }} {{ item.name }}
            </div>
          </div>
          <div class="nav-sep"></div>
          <div class="nav-item" @click="mySubscrition()">我的订阅</div>
          <div class="nav-item" @click="myFavorite()">已收藏</div>
        </nav>
      </div>

      <div class="app">
        <div class="page-body">
          <aside class="sidebar-left">
            <LeftSideBarNewsFeed />
          </aside>
          <!-- MAIN CONTENT -->
          <main class="feed-center">
            <router-view />
          </main>
          <!-- .main -->
          <!-- RIGHT SIDEBAR -->
          <aside class="sidebar-right">
            <RightSideBarNewsFeed />
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
// @ts-ignore
import '@/styles/module_newsfeed.scss';
import AppHeader from '@/components/AppHeader.vue';
import { getNewsFeedMenus, getNewsFeedStyle } from '@/utils/menuUtils.ts';
import { useRouter } from 'vue-router';
import LeftSideBarNewsFeed from '@/views/newsfeed/LeftSideBarNewsFeed.vue';
import RightSideBarNewsFeed from '@/views/newsfeed/RightSideBarNewsFeed.vue';

const moduleStyle = getNewsFeedStyle();

const menuList = getNewsFeedMenus();

const router = useRouter();
const toIndex = () => {
  router.push('/newsfeed');
};

const toNewsList = () => {
  router.push('/newsfeed/list');
};

const mySubscrition = () => {
  router.push('/newsfeed/subscription');
};
const myFavorite = () => {
  router.push('/newsfeed/favorite');
};

const setNav = () => {};
</script>

<style scoped lang="scss"></style>
