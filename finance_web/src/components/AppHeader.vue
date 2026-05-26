<template>
  <!-- Navigation Bar -->
  <div :class="defaultStyle">
    <nav class="mx-auto nav sm:px-6 lg:px-8">
      <div class="nav-left">
        <div
          class="nav-logo"
          style="cursor: pointer"
          @click="navigateTo"
          :data-path="'/'"
          :data-blanktarget="false"
        >
          Venture<span>AI</span>
        </div>
      </div>
      <div class="hidden md:ml-6 md:flex">
        <div class="nav-tabs" v-if="menulist" id="navTabs">
          <div v-for="(item, index) in menulist" :key="index">
            <button
              v-if="route.path.endsWith(item.path)"
              class="nav-tab active"
              :data-path="item.path"
              :data-blanktarget="item.isBlankTarget"
            >
              {{ item?.icon }}{{ item.name }}
            </button>
            <button
              v-else
              class="nav-tab"
              @click="navigateTo"
              :data-path="item.path"
              :data-blanktarget="item.isBlankTarget"
            >
              {{ item?.icon }}{{ item?.name }}
            </button>
          </div>
        </div>
        <div class="subtitle" v-else>{{ subtitle }}</div>
      </div>
      <div class="hidden md:ml-6 md:flex">
        <div class="nav-right">
          <span v-if="!hiddenRightPart">
            <UserStatePanel :cssmodule="defaultStyle" />
          </span>
          <SwitchLanguage @changeEvent="languageChangedEvent" />
        </div>
      </div>

      <!-- Mobile menu button-->
      <div class="md:hidden flex items-center">
        <div class="nav-right">
          <span v-if="!hiddenRightPart">
            <UserStatePanel
              cssmodule="defaultStyle"
              :is-verification="false"
              :display-login-btn="true"
              :display-register-btn="true"
            />
          </span>
          <SwitchLanguage @changeEvent="languageChangedEvent()" />

          <button
            v-if="!hiddenRightPart"
            @click="toggleMenu"
            class="inline-flex p-2 rounded-md text-gray-100 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none"
          >
            <svg
              class="h-6 w-6 p-0 m-0"
              :class="{ hidden: isMenuOpen, block: !isMenuOpen }"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              class="h-6 w-6 p-0 m-0"
              :class="{ block: isMenuOpen, hidden: !isMenuOpen }"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
          <span v-else>
            <BtnReturnHome />
          </span>
        </div>

        <!-- Mobile Menu -->
        <div :class="{ block: isMenuOpen, hidden: !isMenuOpen }" class="md:hidden">
          <div>
            <ul
              class="nav-links-m truncate"
              style="right: 0; background: #5e5b5bff; padding: 5px"
              v-if="menulist"
            >
              <li
                class="px-2 pt-1 mb-1"
                style="height: 25px; color: var(--gold)"
                v-for="(item, index) in menulist"
                :key="index"
                :data-blanktarget="item.isBlankTarget"
                :data-path="item.path"
                @click="m_navigateTo"
              >
                <a href="#" style="color: var(--gold)">{{ item.name }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import '@/styles/module-header.scss';
import {   onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { MenuItem } from '@/utils/menuUtils.ts';
import BtnReturnHome from '@/components/BtnReturnHome.vue';
import UserStatePanel from '@/components/UserStatePanel.vue';
import SwitchLanguage from '@/components/BtnSwitchLanguage.vue';

// 属性
const props = withDefaults(
  defineProps<{
    subtitle: string;
    cssmodule: string;
    displayToken?: boolean;
    menulist?: MenuItem[];
  }>(),
  {
    subtitle: '',
    cssmodule: 'module-default',
    displayToken: false,
    menulist: undefined,
  }
);

const hiddenRightPart = ref(false);
const defaultStyle = ref<string>(props.cssmodule ? props.cssmodule : 'module-default');
const emit = defineEmits(['switchTabEvent']);

const setActiveMenu = (path: string) => {
  for (let i = 0; props.menulist && i < props.menulist.length; i++) {
    if (route.params.id) {
      const menuPathPrefix = props.menulist[i].path.split(':')[0];
      const id = route.params.id.toString();
      if (route.path.endsWith(id) && path.startsWith(menuPathPrefix)) {
        props.menulist[i].path = path;
      }
    }
  }
};

//语法切换组件事件
const languageChangedEvent = () => {
  console.log('语言被修改了');
};

//路由
const router = useRouter();
const route = useRoute();
const displayLoginBtn = ref<boolean>(false);
const displayRegisterBtn = ref<boolean>(false);

watch(route, () => {
  if (route.path.startsWith('/register')) {
    displayLoginBtn.value = true;
    displayRegisterBtn.value = false;
  }
  setActiveMenu(route.path);
});

const openNewWindow = (path: string) => {
   // 1. 解析路由对象，获取完整的 URL 路径
   // 2. 简单校验：确保是内部路径
  const routeData = router.resolve({path});

  const targetUrl = window.location.origin + routeData.href;

  const newWindow = window.open(targetUrl , '_blank');

  if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
    alert('弹出窗口被浏览器拦截，请允许本站弹窗以继续操作。');
  }
};

const navigateTo = (e: any) => {
  const o = e.currentTarget;
  if (o.dataset.blanktarget && o.dataset.blanktarget.toString() == 'true') {
    openNewWindow(o.dataset.path);
  } else {
    router.push(o.dataset.path);
    emit('switchTabEvent', o.dataset.path);
  }
};

const m_navigateTo = (e: any) => {
  const o = e.currentTarget;
  router.push(o.dataset.path);
};

const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

onMounted(() => {
  if (route.path.startsWith('/register') || route.path.startsWith('/login') || route.path.startsWith('/forgetpassword')) {
    hiddenRightPart.value = true;
  }
});

</script>
<style scoped lang="scss">
.nav-logo {
  cursor: pointer;
}
</style>
