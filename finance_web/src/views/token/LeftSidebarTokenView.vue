<template>
  <!-- PROFILE + LEVEL -->
  <div class="profile-card">
    <div class="pc-cover"></div>
    <div class="pc-av">张</div>
    <div class="pc-body">
      <div class="pc-name">张明远</div>
      <div class="pc-role">创业者 · 智链SaaS · Pre-A</div>
      <div class="level-badge">
        <span class="lb-icon">⚡</span>
        <span class="lb-text">LV.3 · 认证合伙人</span>
      </div>
      <div class="level-progress">
        <div class="lp-header">
          <span class="lp-label">距离 LV.4 核心贡献者</span>
          <span class="lp-val" id="lpText">1,840 / 2,000</span>
        </div>
        <div class="lp-bar">
          <div class="lp-fill" id="lpFill" style="width:92%"></div>
        </div>
        <div class="lp-next">还差 <strong style="color:var(--gold)">160 Token</strong> 升级</div>
      </div>
      <div class="stats-grid">
        <div class="sg-item">
          <div class="sg-val" id="totalEarned">4,280</div>
          <div class="sg-label">累计获得</div>
        </div>
        <div class="sg-item">
          <div class="sg-val">2,440</div>
          <div class="sg-label">累计消耗</div>
        </div>
        <div class="sg-item">
          <div class="sg-val">48</div>
          <div class="sg-label">连签天数</div>
        </div>
        <div class="sg-item">
          <div class="sg-val">12</div>
          <div class="sg-label">已解锁成就</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ACHIEVEMENTS -->
  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">🏆 成就徽章</div>
      <div class="wh-more">全部</div>
    </div>
    <div class="ach-list">
      <div class="ach-item">
        <div class="ach-icon" style="background:var(--gold3);">🚀</div>
        <div class="ach-info">
          <div class="ach-name">第一笔投资连接</div>
          <div class="ach-sub">成功联系投资人</div>
        </div>
        <div class="ach-new">NEW</div>
      </div>
      <div class="ach-item">
        <div class="ach-icon" style="background:var(--blue-dim);">📊</div>
        <div class="ach-info">
          <div class="ach-name">数据达人</div>
          <div class="ach-sub">完整填写所有指标</div>
        </div>
      </div>
      <div class="ach-item">
        <div class="ach-icon" style="background:var(--purple-dim);">🌙</div>
        <div class="ach-info">
          <div class="ach-name">深夜创业者</div>
          <div class="ach-sub">凌晨0-4点登录 10次</div>
        </div>
      </div>
      <div class="ach-item ach-locked">
        <div class="ach-icon" style="background:var(--orange-dim);">💰</div>
        <div class="ach-info">
          <div class="ach-name">融资里程碑</div>
          <div class="ach-sub">成功完成一轮融资</div>
        </div>
      </div>
      <div class="ach-item ach-locked">
        <div class="ach-icon" style="background:var(--green-dim);">🤝</div>
        <div class="ach-info">
          <div class="ach-name">生态建设者</div>
          <div class="ach-sub">邀请 10 位活跃用户</div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
</script>

<style scoped>

</style>
