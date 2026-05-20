<template>
  <div class="my-feed-widget">
    <div class="mfw-head">
      <div class="mfw-title">为你精选</div>
      <div class="mfw-badge">3条新</div>
    </div>
    <div class="mfw-item">
      <div class="mfw-reason">📌 与你项目直接相关</div>
      <div class="mfw-headline">飞书知识库 Pro 发布，与智链SaaS功能高度重叠</div>
      <div class="mfw-meta">45分钟前 · 建议关注</div>
    </div>
    <div class="mfw-item">
      <div class="mfw-reason">💰 目标投资人动态</div>
      <div class="mfw-headline">红杉发布报告：你的融资窗口未来18个月</div>
      <div class="mfw-meta">3小时前 · 融资参考</div>
    </div>
    <div class="mfw-item">
      <div class="mfw-reason">📊 赛道市场信号</div>
      <div class="mfw-headline">明势资本新基金：AI+硬科技，与你赛道有交叉</div>
      <div class="mfw-meta">6小时前 · 潜在投资人</div>
    </div>
  </div>

  <div class="insight-card">
    <div class="ic-label">AI MARKET INSIGHT</div>
    <div class="ic-title">本周 AI 企业服务赛道信号分析</div>
    <div class="ic-body" id="insightBody">
      综合本周32条资讯：竞争强度指数上升（飞书+微软同周发布），但融资环境维持积极（红杉白皮书+明势新基金）。<strong style="color:rgba(255,255,255,0.9)">建议：加速完成Pre-A融资，赶在竞品占据认知前建立标杆客户壁垒。</strong>
    </div>
    <div class="ic-tags">
      <div class="ic-tag">竞争加剧</div>
      <div class="ic-tag">融资窗口开启</div>
      <div class="ic-tag">加速时机</div>
    </div>
  </div>

  <div class="sub-widget">
    <div class="sw-title">定制我的信息流</div>
    <div class="sw-desc">选择你关注的话题，AI 每日 7:00 推送个性化早报</div>
    <div class="sw-topics">
      <div class="sw-topic on" onclick="this.classList.toggle('on')">AI行业</div>
      <div class="sw-topic on" onclick="this.classList.toggle('on')">企业SaaS</div>
      <div class="sw-topic on" onclick="this.classList.toggle('on')">融资动态</div>
      <div class="sw-topic" onclick="this.classList.toggle('on')">政策法规</div>
      <div class="sw-topic" onclick="this.classList.toggle('on')">出海资讯</div>
      <div class="sw-topic" onclick="this.classList.toggle('on')">人事变动</div>
      <div class="sw-topic" onclick="this.classList.toggle('on')">竞品动态</div>
      <div class="sw-topic" onclick="this.classList.toggle('on')">投资机构</div>
    </div>
    <button class="sw-save" onclick="this.textContent='✓ 已保存订阅'; setTimeout(()=>this.textContent='保存订阅设置',2000)">保存订阅设置</button>
  </div>

</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">

</style>
