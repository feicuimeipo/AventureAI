<template>
    <div class="hero-content">
      <div class="hero-eyebrow">
        <hr class="hero-line" /> <span>{{$t('corp_logo_title')}} · {{$t('corp_name')}}</span>
      </div>
      <h1 class="hero-title" v-html="$t('hero_title')"></h1>
      <h1 class="hero-title-en" v-html="$t('hero_title_en')"></h1>

      <p class="hero-slogan" data-zh="">{{$t("hero_slogan")}}</p>
      <p class="hero-slogan-en" data-en="">{{$t("hero_slogan_en")}}</p>
      <div class="hero-actions" >
        <a href="#download_app" class="btn-primary" data-zh="">{{ $t('download_app') }}</a>
        <a href="#about" class="btn-ghost" data-zh="">{{$t('learn_more')}}</a>
      </div>
    </div>
</template>

<script setup lang="ts">

</script>


<style scoped lang="scss">


.hero-actions{
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 40px;
}



.hero-content{
  position: relative;
  z-index: 1;
  /*max-width: 760px;*/
}

.hero-eyebrow{
  font-size: var(--font-size-base);
  letter-spacing: 0.2em;
  color: var(--gold);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}


.hero-line{
  width: 30px;
  height: 1px;
  margin-left: 10px;
  color: var(--gold);
}

.hero-title {
  font-size: clamp(38px, 6vw, 72px);
  font-weight: 600;
  line-height: 1.15;
  color: var(--cream);
  margin-bottom: 8px;
  letter-spacing: -0.01em;
  width: 55%;
}

.hero-title-en{
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(28px, 4vw, 52px);
  font-weight: 300;
  font-style: italic;
  color: var(--muted);
  margin-bottom: 32px;
  letter-spacing: -0.02em;
  width: 85%;
}

.hero-slogan{
  font-size: var(--font-size-16);
  color: var(--cream2);
  line-height: 1.8;
  max-width: 540px;
  margin-bottom: 10px;
}

.hero-slogan-en{
  font-family: 'Cormorant Garamond', serif;
  font-size: var(--font-size-16);
  font-style: italic;
  color: var(--muted);
  margin-bottom: 48px;
  letter-spacing: 0.02em;
}

</style>
