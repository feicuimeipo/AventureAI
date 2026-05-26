<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SwitchLanguage from '@/components/BtnSwitchLanguage.vue';
import { getHomeMenus, getHomeModuleStyle, type MenuItem } from '@/utils/menuUtils.ts';
import { useI18n } from 'vue-i18n';
import MyButton from '@/components/MyButton.vue';
import UserStatePanel from '@/components/UserStatePanel.vue';

withDefaults(
  defineProps<{
    cssmodule?: string | 'default-module';
  }>(),
  { cssmodule: getHomeModuleStyle() }
);

const { t } = useI18n();

const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const menuList = ref<MenuItem[]>(getHomeMenus(t));
const languageChangedEvent = () => {
  menuList.value = getHomeMenus(t);
};

const router = useRouter()
const switchTo = (routePath:string) =>{
  router.push(routePath)
}
</script>

<template>
  <!-- Navigation Bar -->
  <nav :class="cssmodule">
    <div class="mx-auto px-4 sm:px-6 lg:px-8" style="width: 100%">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="shrink-0 flex items-center">
          <a class="nav-logo" href="/">
            <div class="nav-logo-mark">YY</div>
            <div class="nav-logo">Venture<span>资本</span></div>
          </a>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:ml-6 md:flex md:items-center md:space-x-8">
          <ul class="nav-links">
            <li v-for="(item, index) in menuList" :key="index">
              <router-link
                :to="{ path: '/', hash: item.path }"
                class="nav-links"
                active-class="active"
              >
                {{ item.name }}
              </router-link>
              <!--               <a href="{{ item.path }}" >{{ item.name }}</a>-->
            </li>
          </ul>
        </div>

        <div class="hidden md:ml-6 md:flex items-center md:space-x-8 gap-2">
          <UserStatePanel
            cssmodule="defaultStyle"
            :is-verification="false"
            :display-login-btn="true"
            :display-register-btn="true"
          />
          <MyButton
            id="btnGoPartner"
            label="创业搭子"
            path="/partner"
            fontStyle="font-weight:bold"
          />
          <MyButton
            id="btnGoPlatform"
            label="控制台"
            path="/platform"
            fontStyle="font-weight:bold"
          />
          <SwitchLanguage @changeEvent="languageChangedEvent()" />
        </div>

        <!-- Mobile menu button-->
        <div class="md:hidden flex items-center">
          <UserStatePanel
            cssmodule="defaultStyle"
            :is-verification="false"
            :display-login-btn="true"
            :display-register-btn="true"
          />
          <SwitchLanguage @changeEvent="languageChangedEvent()" />
          <button
            @click="toggleMenu"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-100 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none"
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
              class="h-6 w-6 p-0 m-0 px-10"
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
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div :class="{ block: isMenuOpen, hidden: !isMenuOpen }" class="md:hidden">
      <div class="p-0 m-0">
        <ul class="nav-links-m" style="width: 80px; top: 5px">
          <li class="px-2 pt-1" style="height: 25px" v-for="(item, index) in menuList" :key="index">
            <a href="{{ item.path }}">{{ item.name }}</a>
          </li>
          <li class="px-2 pt-1" style="height: 25px">
            <a href="#" @click="switchTo('/partner/discovery')">匹配搭子</a>
          </li>
          <li class="px-2 pt-1" style="height: 25px">
            <a href="#" @clicn="switchTo('/platform/profile')">控制台</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 0 1vw;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--line);
  transition: all 0.3s;
  background: var(--ink);
  box-shadow: var(--ink3) 0 1px 0;
}

.nav-logo-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  line-height: 35px;
  border: 1.5px solid var(--gold);
  border-radius: 6px;
  font-size: var(--font-size-14);
  font-weight: 500;
  color: var(--gold);
  letter-spacing: -0.05rem;
}

.nav-logo {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 0.1rem;
  color: var(--gold);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-logo span {
  color: white;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 32px;
  list-style: none;
  text-transform: uppercase;
  margin-top: 8px;
}

.nav-links:hover {
  color: var(--white);
}

.nav-links:active {
  color: var(--white);
}

.nav-links a {
  text-transform: uppercase;
}

.login-register a {
  text-transform: capitalize;
}

.nav-links a,
.login-register a {
  font-size: var(--font-size-base);
  letter-spacing: 0.01em;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s;
}

.nav-links-m {
  margin-top: 100px;
  list-style: none;
  padding: 0;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-links-m li {
  margin-top: 2px;
  background: var(--gold-dim);
}

.nav-links-m a {
  font-size: var(--font-size-base);
  letter-spacing: 0.01em;
  text-decoration: none;
  transition: color 0.2s;
  text-transform: uppercase;
  color: var(--gold);
}

</style>
