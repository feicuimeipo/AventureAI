<template>
  <div :class="moduleStyle">
    <div class="shell">
      <!-- TOP BAR -->
      <div class="top-bar">
          <AppHeader subtitle="" :cssmodule="moduleStyle" :menulist=menuList  @switchTabEvent="handleSwitchTab"  :is-verification=true />
      </div>

      <!-- CONTENT -->
      <div class="content-area">
          <router-view />
      </div>

      <!-- BOTTOM BAR -->
      <div class="bottom-bar">
        <PlatformBottomBar />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import "@/styles/module-platform.scss"
import AppHeader from "@/components/AppHeader.vue";
import {ref} from "vue";
import PlatformBottomBar from "@/views/platform/PlatformBottomBar.vue";
import {getPlatformSyleClass} from "@/utils/menuUtils.ts";
import {getPlatformMenus} from "@/utils/menuUtils.ts";

const moduleStyle = ref<string>(getPlatformSyleClass())

const menuList = getPlatformMenus()
const handleSwitchTab = (path:string) => {
   console.log("选择一个菜单:"+path)
}
</script>

<style scoped>

</style>
