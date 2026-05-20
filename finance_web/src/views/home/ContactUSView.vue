<script setup lang="ts"></script>

<template>
  <div>
    <div class="section-label" data-zh="">{{ $t('contact_us') }}</div>
    <h2 class="section-title" data-zh="">{{ $t('contact_us_title') }}</h2>
    <p class="section-title-en" data-zh="">{{ $t('contact_us_subtitle') }}</p>
    <p class="contact-desc" data-zh="">{{ $t('contact_us_body') }}</p>

    <div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
      <div class="contact-left">
        <div class="contact-methods">
          <a class="contact-item" href="mailto:contact@yoluyoru.cn">
            <div class="contact-icon">✉️</div>
            <div class="contact-info">
              <div class="contact-type">Email</div>
              <div class="contact-value">contact@yoluyoru.cn</div>
            </div>
          </a>
          <a class="contact-item" href="#">
            <div class="contact-icon">💬</div>
            <div class="contact-info">
              <div class="contact-type">WeChat <span data-zh="">微信</span></div>
              <div class="contact-value">yoluyoru_capital</div>
            </div>
          </a>
          <a class="contact-item" href="https://wa.me/yoluyoru" target="_blank">
            <div class="contact-icon">📱</div>
            <div class="contact-info">
              <div class="contact-type">WhatsApp</div>
              <div class="contact-value" data-zh="">{{ $t('contact_us_method_whatsapp') }}</div>
            </div>
          </a>
        </div>
      </div>

      <div class="contact-right">
        <div class="map-placeholder">
          <div class="map-inner">
            <span class="map-pin">📍</span>
            <div class="map-loc" data-zh="">{{ $t('contact_us_location') }}</div>
            <div class="map-loc-sub" data-zh="">{{ $t('corp_name') }}</div>
            <div class="map-loc-sub" data-en="">{{ $t('corp_name_en') }}</div>
            <div class="domain">yoluyoru.cn</div>
          </div>
        </div>

        <div>
          <div class="follow_us" data-zh="">关注我们</div>
          <div class="follow_us" data-en="">Follow Us</div>
          <div class="social-links">
            <a class="social-btn" href="#"><span>📕</span>{{ $t('follow_us_redbook') }}</a>
            <a class="social-btn" href="#"><span>▶</span>{{ $t('follow_us_tiktok') }}</a>
            <a class="social-btn" href="#"><span>𝕏</span>{{ $t('follow_us_twitter') }}</a>
            <a class="social-btn" href="#"><span>in</span>{{ $t('follow_us_linkedin') }}</a>
            <a class="social-btn" href="#"><span>🎙</span>{{ $t('follow_us_little_universe') }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
section {
  padding: 100px 5vw;
  position: relative;
  z-index: 1;
}
.section-label {
  font-size: 10px;
  letter-spacing: 0.22em;
  color: var(--gold);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.section-label-line {
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
  font-size: clamp(18px, 2.5vw, 28px);
  font-weight: 300;
  font-style: italic;
  color: var(--muted);
  margin-bottom: 40px;
  letter-spacing: 0.02em;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: start;
  margin-top: 56px;
}
.contact-desc {
  font-size: var(--font-size-16);
  line-height: 1.9;
  margin-bottom: 40px;
  color: rgba(240, 233, 220, 0.7);
}

.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 18px 20px;
  background: var(--ink2);
  border: 1px solid var(--line);
  border-radius: 3px;
  transition: all 0.2s;
  text-decoration: none;
}

.contact-item:hover {
  background-color: var(--gold-dim);
  border: 1px solid var(--gold);
}

.contact-type {
  color: var(--gold);
  font-size: var(--font-size-16);
}

.contact-right {
  background: var(--ink2);
  border: 1px solid var(--line);
  padding: 40px 36px;
  border-radius: 3px;
}

.map-placeholder {
  width: 100%;
  aspect-ratio: 4/3;
  background: var(--ink3);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  border: 1px solid var(--line2);
  position: relative;
  overflow: hidden;
}

.map-inner {
  text-align: center;
}

.map-pin {
  font-size: 28px;
  display: block;
  margin-bottom: 8px;
}

.map-loc {
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--gold);
  text-transform: uppercase;
}

.map-loc-sub {
  font-size: 12px;
  color: var(--muted);
  margin-top: 4px;
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
}

.social-links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.social-btn {
  font-size: 9px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 8px 16px;
  border-radius: 2px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.domain {
  margin-top: 16px;
  font-size: 12px;
  color: var(--muted2);
}
.follow_us {
  font-size: 10px;
  letter-spacing: 0.15em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 12px;
}
</style>