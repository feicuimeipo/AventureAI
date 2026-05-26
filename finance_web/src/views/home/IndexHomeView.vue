<script setup lang="ts">
import AboutView from '@/views/home/AboutView.vue';
import PlatformValueView from '@/views/home/ValueView.vue';
import TeamView from '@/views/home/TeamView.vue';
import DownloadAppView from '@/views/home/DownloadView.vue';
import ContactUSView from '@/views/home/ContactUSView.vue';
import HeroView from '@/views/home/HeroView.vue';
import HomeHeader from '@/components/HomeHeader.vue';
import HomeFooter from '@/components/HomeFooter.vue';
import { getHomeModuleStyle } from '@/utils/menuUtils.ts';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <HomeHeader :cssmodule="getHomeModuleStyle()" />
    <!-- Main Content -->
    <main>
      <section class="hero">
        <HeroView />
      </section>
      <div class="section-sep"></div>
      <section id="about">
        <AboutView />
      </section>

      <div class="section-sep"></div>
      <section id="values" class="values-section">
        <PlatformValueView />
      </section>

      <div class="section-sep"></div>
      <section id="team">
        <TeamView />
      </section>

      <div class="section-sep"></div>
      <section id="download_app" class="app-section">
        <DownloadAppView />
      </section>
      <div class="section-sep"></div>
      <section id="contact">
        <ContactUSView />
      </section>
    </main>
    <HomeFooter />
  </div>
</template>

<style scoped lang="scss">
main {
  background-color: var(--ink);
}

section {
  padding: 100px 5vw;
}

.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 120px 5vw 80px;
}

.section-label {
  font-size: var(--font-size-base);
  letter-spacing: 0.2em;
  color: var(--gold);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.session-line {
  width: 30px;
  height: 1px;
  margin-left: 10px;
  color: var(--gold);
}

.section-sep {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-line), transparent);
  margin: 0 5vw;
  width: calc(100% - 10vw);
}
.router-link-active {
  background-color: #4f46e5; /* bg-indigo-600 的具体色值 */
  color: #ffffff;            /* text-white 的具体色值 */
}
</style>
