<template>

    <div class="section-label">
      <hr class="section-label-line" />
      <span>{{$t('platform_value')}}</span>
    </div>

    <h2 class="section-title" >{{$t('platform_value_title')}}</h2>
    <h2 class="section-title-en">{{$t('platform_value_title_en')}}</h2>

    <div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
      <div class="value-card fade-in visible">
        <span class="value-icon">🎯</span>
        <span class="value-num">01</span>
        <div class="value-title" >{{$t('value_title_1')}}</div>
        <span class="value-title-en" >{{$t('value_title_1_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_1_slogan')}}</span>
        <p class="value-desc" >{{$t('value_title_1_desc')}}</p>
      </div>
      <div class="value-card fade-in visible">
        <span class="value-icon">📡</span>
        <span class="value-num">02</span>
        <div class="value-title" >{{$t('value_title_2')}}</div>
        <span class="value-title-en" >{{$t('value_title_2_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_2_slogan')}}</span>
        <p class="value-desc" >{{$t('value_title_2_desc')}}</p>
      </div>
      <div class="value-card fade-in visible">
        <span class="value-icon">🤝</span>
        <span class="value-num">03</span>

        <div class="value-title" >{{$t('value_title_3')}}</div>
        <span class="value-title-en" >{{$t('value_title_3_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_3_slogan')}}</span>
        <p class="value-desc" >{{$t('value_title_3_desc')}}</p>

       </div>
      <div class="value-card fade-in visible">
        <span class="value-icon">🏢</span>
        <span class="value-num">04</span>

        <div class="value-title" >{{$t('value_title_4')}}</div>
        <span class="value-title-en" >{{$t('value_title_4_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_4_slogan')}}</span>
        <p class="value-desc" >{{ $t('value_title_4_desc')}}</p>

      </div>
      <div class="value-card fade-in visible">
        <span class="value-icon">⬡</span>
        <span class="value-num">05</span>

        <div class="value-title" >{{$t('value_title_5')}}</div>
        <span class="value-title-en" >{{$t('value_title_5_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_5_slogan')}}</span>
        <p class="value-desc" >{{$t('value_title_5_desc')}}</p>

      </div>
      <div class="value-card fade-in visible">
        <span class="value-icon">🌐</span>
        <span class="value-num">06</span>

        <div class="value-title" >{{$t('value_title_6')}}</div>
        <span class="value-title-en" >{{$t('value_title_6_subtitle')}}</span>
        <span class="value-title-en" >{{$t('value_title_6_slogan')}}</span>
        <p class="value-desc" >{{$t('value_title_6_desc')}}</p>
      </div>
    </div>

</template>

<script setup lang="ts">

</script>

<style scoped>
section {
  padding: 100px 5vw;
  position: relative;
}
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

/*可以做的事*/
.value-card {
  background: var(--ink2);
  padding: 40px 32px;
  border-top: 2px solid transparent;
  transition: all 0.3s;
  position: relative;
}

.value-card:hover{
  border-top: 2px solid var(--gold);
  background-color: var(--gold-dim);
}


.value-icon {
  font-size: 24px;
  margin-bottom: 20px;
  display: block;
}
.value-num {
  font-size: 10px;
  letter-spacing: 0.18em;
  color: var(--gold);
  margin-bottom: 14px;
  display: block;
}
.value-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--cream);
  margin-bottom: 6px;
}
.value-title-en {
  font-family: 'Cormorant Garamond', serif;
  font-size: var(--font-size-base);
  font-style: italic;
  color: var(--muted);
  margin-bottom: 16px;
  display: block;
  letter-spacing: 0.04em;
}

.value-desc {
  font-size: var(--font-size-base);
  color: rgba(240,233,220,0.6);
  line-height: 1.85;
}

</style>
