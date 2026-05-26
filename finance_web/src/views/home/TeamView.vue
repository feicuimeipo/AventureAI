<template>
  <div class="section-label">
    <hr class="section-label-line" />
    <span>{{$t('our_team')}}</span>
  </div>

  <h2 class="section-title" >{{$t('team_title')}}</h2>
  <h2 class="section-title-en">{{$t('team_title_subtitle')}}</h2>

  <div class="team-grid grid grid-cols-1 md:grid-cols-1 lg:grid-cols-4 gap-1">
    <div class="team-card fade-in visible">
      <div class="team-avatar">{{$t('team_avatar_1')}}</div>
      <div class="team-name" >{{$t('team_avatar_1_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_1_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_1_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_1_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_1_tags_2')}}</span>
      </div>
    </div>
    <div class="team-card fade-in visible">
      <div class="team-avatar">{{$t('team_avatar_2')}}</div>
      <div class="team-name" >{{$t('team_avatar_2_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_2_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_2_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_2_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_2_tags_2')}}</span>
      </div>
    </div>
    <div class="team-card fade-in visible">
      <div class="team-avatar">{{$t('team_avatar_3')}}</div>
      <div class="team-name" >{{$t('team_avatar_3_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_3_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_3_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_3_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_3_tags_2')}}</span>
      </div>
    </div>
    <div class="team-card fade-in visible">
      <div class="team-avatar">{{$t('team_avatar_4')}}</div>
      <div class="team-name" >{{$t('team_avatar_4_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_4_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_4_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_4_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_4_tags_2')}}</span>
      </div>
    </div>
    <div class="team-card fade-in visible" style="grid-column: span 2;">
      <div class="team-avatar">{{$t('team_avatar_5')}}</div>
      <div class="team-name" >{{$t('team_avatar_5_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_5_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_5_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_5_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_5_tags_2')}}</span>
        <span class="team-tag">{{$t('team_avatar_5_tags_3')}}</span>
        <span class="team-tag">{{$t('team_avatar_5_tags_4')}}</span>
      </div>
    </div>
    <div class="team-card fade-in visible" style="grid-column: span 2;">
      <div class="team-avatar">{{$t('team_avatar_6')}}</div>
      <div class="team-name" >{{$t('team_avatar_6_name')}}</div>
      <div class="team-role" >{{$t('team_avatar_6_role')}}</div>
      <p class="team-bg" >{{$t('team_avatar_6_bg')}}</p>
      <div class="team-tags">
        <span class="team-tag">{{$t('team_avatar_6_tags_1')}}</span>
        <span class="team-tag">{{$t('team_avatar_6_tags_2')}}</span>
        <span class="team-tag">{{$t('team_avatar_6_tags_3')}}</span>
        <span class="team-tag">{{$t('team_avatar_6_tags_4')}}</span>
        <span class="team-tag">{{$t('team_avatar_6_tags_5')}}</span>
        <span class="team-tag">{{$t('team_avatar_6_tags_6')}}</span>
      </div>
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
  font-family: var(--mono);
  font-size: 9px;
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
  font-family: var(--serif);
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

.section-body {
  font-size: 15px;
  color: rgba(240,233,220,0.7);
  line-height: 1.9;
  max-width: 680px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--line);
  margin-top: 56px;
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


.team-card {
  background: var(--ink2);
  padding: 32px 24px;
  transition: all 0.25s;
  position: relative;
  overflow: hidden;
}
.team-card:hover{
  background-color: var(--gold-dim);
  border-bottom: 2px solid var(--gold);
}

.team-avatar {
  width: 52px;
  height: 52px;
  border-radius: 6px;
  background: var(--gold-dim);
  border: 1px solid var(--gold-line);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--serif);
  font-size: 20px;
  font-weight: 600;
  color: var(--gold);
  margin-bottom: 20px;
}

.team-name {
  font-family: var(--serif);
  font-size: var(--font-size-16);
  font-weight: 600;
  color: var(--cream);
  margin-bottom: 4px;
}

.team-role {
  font-family: var(--mono);
  font-size: var(--font-size-label);
  letter-spacing: 0.1em;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 12px;
}
.team-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 14px;
}

.team-tag {
  font-family: var(--mono);
  font-size: 8px;
  letter-spacing: 0.1em;
  color: var(--muted);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 3px 8px;
  border-radius: 2px;
  text-transform: uppercase;
}
</style>
