<template>
<!-- ── ABOUT ── -->
    <div class="section-label">
      <hr class="section-label-line" />
      <span>{{$t('about_us')}}</span>
    </div>
    <h2 class="section-title">{{$t('about_us_title')}}</h2>
    <h2 class="section-title-en">{{$t('about_us_title_en')}}</h2>

    <div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 gap-8 mb-16" >
      <div class="about-text fade-in visible">
        <p>{{$t('about_us_content_1')}}</p>
        <p>{{$t('about_us_content_2')}}</p>
        <p>{{$t('about_us_content_3')}}</p>
      </div>
      <div class="fade-in visible">
        <div class="about-stats">
          <div class="stat-item">
            <span class="stat-num">2,700+</span>
            <span class="stat-label">{{$t('about_us_stats_seed_user')}}</span>
            <span class="stat-label-en">{{$t('about_us_stats_seed_user_en')}}</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">8+</span>
            <span class="stat-label" >{{$t('about_us_stats_enterprise_client')}}</span>
            <span class="stat-label-en" >{{$t('about_us_stats_enterprise_client_en')}}</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">8人</span>
            <span class="stat-label" data-zh="">{{$t('about_us_stats_core_team_member')}}</span>
            <span class="stat-label-en" >{{$t('about_us_stats_core_team_member_en')}}</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">5</span>
            <span class="stat-label" data-zh="">{{$t('about_us_stats_core_ai_core_modules')}}</span>
            <span class="stat-label-en" >{{$t('about_us_stats_core_ai_core_modules_en')}}</span>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup  lang="ts">

</script>

<style scoped lang="scss">

.section-label {

  font-size: var(--font-size-base);
  letter-spacing: 0.22em;
  color: var(--gold);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.section-label-line{
  width: 30px;
  height: 1px;
  margin-left: 10px;
  color: var(--gold);
}

.section-title {
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 600;
  line-height: 1.25;
  color: var(--cream);
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.section-title-en {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(18px, 2.5vw, 28px);
  font-weight: 300;
  font-style: italic;
  color: var(--muted);
  margin-bottom: 40px;
  letter-spacing: 0.02em;
}

.about-grid {
  //display: grid;
  //grid-template-columns: 1fr 1fr;
  gap: 60px;
  margin-top: 48px;
  align-items: start;
}


.fade-in {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
  font-size: var(--font-size-14);
  color: var(--cream3);
  line-height: 30px; /* 百分比行距 */
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

.fade-in p{
  padding-bottom: 30px;
}

/*统计*/
.about-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--line);
}

.stat-item {
  background: var(--ink2);
  padding: 28px 24px;
  transition: background 0.2s;
}

.stat-item:hover {
  background: var(--gold-dim);
}

.stat-num {
  font-size: 32px;
  color: var(--gold);
  display: block;
  margin-bottom: 6px;
  letter-spacing: -0.02em;
  font-weight: bold;
}

.stat-label {
  font-size: var(--font-size-base);
  color: var(--muted);
  letter-spacing: 0.06em;

}

.stat-label-en {
  font-size: 10px;
  color: var(--muted2);
  letter-spacing: 0.04em;
  font-style: italic;
  display: block;
  margin-top: 3px;
  font-family: 'Cormorant Garamond', serif;
}
</style>
