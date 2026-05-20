<template>
  <div :class="styleModule" >
    <div class="news-layout">
      <div class="news-nav">
        <div class="nn-logo">行业动态</div>
        <div class="nn-item on">📡 全部动态 <span class="badge">24</span></div>
        <div class="nn-item">🤖 AI · 大模型 <span class="badge">8</span></div>
        <div class="nn-item">💰 融资新闻</div>
        <div class="nn-item">🏢 企业服务</div>
        <div class="nn-item">📈 我订阅的</div>
        <div style="margin:16px 18px 10px;font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.1em;color:#7a7568;">广告合作方</div>
        <div class="nn-item" style="font-size:12px;opacity:0.7;">💼 京东金融</div>
        <div class="nn-item" style="font-size:12px;opacity:0.7;">🛒 阿里巴巴</div>
        <div class="nn-item" style="font-size:12px;opacity:0.7;">🔍 百度</div>
        <div class="nn-item" style="font-size:12px;opacity:0.5;">+ 易方达基金</div>
        <div class="nn-item" style="font-size:12px;opacity:0.5;">+ 美的科技</div>
      </div>
      <div class="news-feed">
        <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.14em;color:#7a7568;margin-bottom:14px;">MODULE 04 · 行业动态 + 社区讨论</div>
        <div class="news-digest">
          <div class="nd-head"><div class="nd-dot"></div>AI 今日摘要 · 为张明远定制</div>
          <div class="nd-text">今日企业AI领域3个重要信号：① <strong>微软Copilot</strong>在企业知识管理场景NPS达82，印证你的赛道价值；② 竞品<strong>Notion AI</strong>完成$1.5亿C轮，估值溢价暗示市场升温；③ 你关注的<strong>李嘉玲</strong>刚转发了一篇关于RAG落地的深度文章——触达时机极佳。</div>
        </div>
        <div class="news-article">
          <div class="na-meta"><span>36氪</span><span>·</span><span>2小时前</span><span>·</span><span style="color:var(--gold);">与你高度相关</span></div>
          <div class="na-title">Notion AI完成$1.5亿C轮，企业知识管理赛道迎来新一轮资本涌入</div>
          <div class="na-excerpt">本轮估值较上轮提升240%，多名VC表示"企业AI化知识管理是2024年最确定的方向之一"，市场空间预计超过$500亿……</div>
          <div class="na-tags"><span class="na-tag gold">竞品融资</span><span class="na-tag">企业AI</span><span class="na-tag">SaaS</span></div>
        </div>
        <div class="news-article">
          <div class="na-meta"><span>虎嗅</span><span>·</span><span>4小时前</span></div>
          <div class="na-title">红杉中国最新LP信：今年重点关注To B AI落地，回报周期比C端短3-5年</div>
          <div class="na-excerpt">李嘉玲在内部分享会中强调，企业服务AI的标准化程度决定估值天花板，有数据沉淀的公司将获得3-5x估值溢价……</div>
          <div class="na-tags"><span class="na-tag gold">投资人动态</span><span class="na-tag">红杉</span></div>
        </div>
      </div>
      <div class="news-sidebar">
        <div class="ns-widget">
          <div class="ns-widget-title" style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.1em;color:#7a7568;">💬 投资人在讨论</div>
          <div class="comment-item">
            <div class="ci-top">
              <div class="ci-av" style="background:#1a2a3a;color:#63b3ed;">李</div>
              <span class="ci-name" style="color:#1a1612;">李嘉玲</span>
              <span class="ci-role" style="background:#1a3a5c;">投资人</span>
            </div>
            <div class="ci-text" style="color:#3d3830;">RAG在企业场景的核心不是技术，是数据飞轮。谁先建立起数据壁垒，谁就赢了。</div>
          </div>
          <div class="comment-item">
            <div class="ci-top">
              <div class="ci-av" style="background:#2a1a2a;color:#b794f4;">王</div>
              <span class="ci-name" style="color:#1a1612;">王思远 IDG</span>
              <span class="ci-role" style="background:#2a1a5c;">VC</span>
            </div>
            <div class="ci-text" style="color:#3d3830;">企业知识管理的迁移成本是天然护城河，一旦接入就很难换掉。</div>
          </div>
        </div>
        <div style="background:rgba(201,146,74,0.06);border:1px solid rgba(201,146,74,0.15);border-radius:6px;padding:12px;margin-bottom:12px;">
          <div style="font-family:'DM Mono',monospace;font-size:9px;color:var(--gold);margin-bottom:6px;letter-spacing:0.08em;">SPONSORED · 京东金融</div>
          <div style="font-size:12px;color:#3d3830;line-height:1.6;">为科技创业者提供最高500万创业贷款，无抵押，48小时放款。</div>
          <div style="font-size:10px;color:var(--gold);margin-top:6px;cursor:pointer;">了解详情 →</div>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.1em;color:#7a7568;margin-bottom:8px;">平台广告收入示意</div>
        <div style="background:#f2ede4;border-radius:4px;padding:12px;font-size:11px;color:#7a7568;line-height:1.7;">
          当前合作广告主：<br>
          <span style="color:var(--gold);">京东金融 · 阿里 · 百度</span><br>
          <span style="color:var(--gold);">易方达基金 · 美的科技</span><br>
          <span style="color:var(--gold);">脉脉 · 欧易</span><br>
          精准投放至<strong>匹配用户画像</strong>，CPM溢价3-5x
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {getPlatformSyleClass} from "@/utils/menuUtils.ts";
 const styleModule = getPlatformSyleClass();
</script>

<style scoped lang="scss">
.module-newsfeed,
.module-token,
.module-platform,
.module-default{
  all:unset
}
</style>
