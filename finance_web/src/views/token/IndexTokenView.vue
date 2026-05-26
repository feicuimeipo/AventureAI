<template>


  <div class="min-h-screen module-token">
    <AppHeader subtitle="" cssmodule="module-token" :display-token=true />

    <!-- TOAST -->
    <MyToastPanel />


    <div class="page">
      <!-- ══ LEFT ══ -->
      <aside class="left-col">
        <LeftSidebarTokenView />
      </aside>

      <!-- MAIN CONTENT -->
      <main class="center-col">
          <RouterView />
      </main><!-- .main -->
      <!-- ══ RIGHT ══ -->
      <aside class="right-col">
          <RightSidebarTokenView />
      </aside>
    </div><!-- .app -->
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import '@/styles/module_token.scss'
import AppHeader from "@/components/AppHeader.vue";
import LeftSidebarTokenView from "@/views/token/LeftSidebarTokenView.vue";
import RightSidebarTokenView from "@/views/token/RightSidebarTokenView.vue";
import MyToastPanel from "@/views/token/ToastForToken.tsx";

</script>

<style scoped>

</style>
