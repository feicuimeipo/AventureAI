<template>

  <div class="section-label">
    <hr class="section-label-line" />
    <span>{{$t('download_app')}}</span>
  </div>
  <h2 class="section-title" >{{$t('download_app_title')}}</h2>
  <h2 class="section-title-en">{{$t('download_app_subtitle')}}</h2>
  <p class="section-body">{{$t('download_app_body')}}</p>
  <br/><br/>
  <ul class="app-features">
    <li><span style="color: var(--gold)">→</span> {{$t('download_app_features_1')}}</li>
    <li><span style="color: var(--gold)">→</span>{{$t('download_app_features_2')}}</li>
    <li><span style="color: var(--gold)">→</span> {{$t('download_app_features_3')}}</li>
    <li><span style="color: var(--gold)">→</span> {{$t('download_app_features_4')}}</li>
    <li><span style="color: var(--gold)">→</span> {{$t('download_app_features_5')}}</li>
  </ul>
  <br/><br/>
  <div class="qr-cluster">
    <!-- iOS QR -->
    <div class="qr-item">
      <div class="qr-box">
        <!-- QR Pattern Placeholder -->
        <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Corner squares -->
          <rect x="5" y="5" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="9" y="9" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="13" y="13" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <rect x="67" y="5" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="71" y="9" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="75" y="13" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="67" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="9" y="71" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="13" y="75" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <!-- Data modules (simplified pattern) -->
          <rect x="40" y="5" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="5" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="15" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="55" y="15" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="45" y="25" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="40" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="15" y="40" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="50" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="20" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="40" width="55" height="6" rx="1" fill="#C8883C"></rect>
          <rect x="40" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="50" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="70" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="55" y="70" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="70" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="80" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="80" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="80" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="80" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="90" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="60" y="90" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="70" y="90" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <!-- YOLUYORU center mark -->
          <rect x="44" y="44" width="12" height="12" rx="2" fill="#C8883C"></rect>
        </svg>
      </div>
      <div class="qr-label" data-zh="">iOS 下载</div>
      <div class="qr-label" data-en="">iOS Download</div>
      <div class="qr-sub">App Store</div>
    </div>
    <!-- Android QR -->
    <div class="qr-item">
      <div class="qr-box">
        <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="5" y="5" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="9" y="9" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="13" y="13" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <rect x="67" y="5" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="71" y="9" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="75" y="13" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="67" width="28" height="28" rx="3" fill="#0A0806"></rect>
          <rect x="9" y="71" width="20" height="20" rx="2" fill="white"></rect>
          <rect x="13" y="75" width="12" height="12" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="5" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="55" y="5" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="45" y="15" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="55" y="25" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="25" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="40" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="20" y="40" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="10" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="20" y="50" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="5" y="60" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="40" y="40" width="6" height="55" rx="1" fill="#C8883C"></rect>
          <rect x="50" y="40" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="60" y="40" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="40" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="50" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="50" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="60" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="60" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="70" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="70" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="70" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="80" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="80" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="50" y="90" width="10" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="65" y="90" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="75" y="90" width="6" height="6" rx="1" fill="#0A0806"></rect>
          <rect x="44" y="44" width="12" height="12" rx="2" fill="#C8883C"></rect>
        </svg>
      </div>
      <div class="qr-label" data-zh="">Android 下载</div>
      <div class="qr-label" data-en="">Android Download</div>
      <div class="qr-sub">Google Play / APK</div>
    </div>
  </div>

</template>

<script setup lang="ts">

</script>

<style scoped>

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
  font-size: clamp(18px, 2.5vw, 28px);
  font-weight: 300;
  font-style: italic;
  color: var(--muted);
  margin-bottom: 40px;
  letter-spacing: 0.02em;
}

.section-body {
  font-size: var(--font-size-16);
  color: rgba(240,233,220,0.7);
  line-height: 1.9;
  max-width: 680px;
}

.app-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 32px;
}

.app-features li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: var(--font-size-base);
  color: var(--muted);
  line-height: 1.6;
}

.qr-cluster {
  display: flex;
  gap: 20px;
}

.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.qr-box {
  width: 120px;
  height: 120px;
  background: var(--cream);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--gold-line);
}

.qr-label {
  font-size: var(--font-size-label);
  letter-spacing: 0.1em;
  color: var(--muted);
  text-align: center;
  text-transform: uppercase;
}

.qr-sub {
  font-size: var(--font-size-label);
  color: var(--muted2);
  text-align: center;
  font-style: italic;
  font-family: 'Cormorant Garamond', serif;
}


</style>
