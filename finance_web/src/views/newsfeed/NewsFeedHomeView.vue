<template>
  <!-- AI DAILY DIGEST -->
  <div class="digest-banner" id="digestBanner">
    <div class="db-label">AI MORNING BRIEF · 今日摘要 · <span id="digestTime"></span></div>
    <div class="db-title">今日创投圈：AI Agent 商业化提速，三家大模型公司完成融资</div>
    <div class="db-content" id="digestContent">
      今日创投圈焦点集中在 AI 商业化赛道：Anthropic
      完成新一轮15亿美元融资，估值突破400亿美元，创下AI公司单轮融资新高；与此同时，国内三家 AI Agent
      方向创业公司宣告完成Pre-A融资，标志着该方向进入加速期。<br /><br />
      政策面，国家互联网信息办公室就《生成式AI服务管理办法》修订版征求意见，重点新增对AI生成内容标注的强制性要求，对企业合规成本影响值得关注。<br /><br />
      <strong style="color: rgba(255, 255, 255, 0.9)">与你相关</strong
      >：字节跳动企业知识管理方向有新产品发布，系你的直接竞品；红杉中国昨日发布AI+企业服务赛道投研报告，结论对你的融资时间窗口判断有参考价值。
    </div>
    <div class="db-footer">
      <div class="db-meta" id="digestMeta">AI摘要 · 覆盖今日 47 条资讯 · 7:02 生成</div>
      <button class="db-refresh" id="refreshBtn" onclick="refreshDigest()">↻ 重新生成</button>
    </div>
  </div>

  <!-- FEATURED -->
  <div
    class="article-featured"
    @click="openArticle"
    style="animation: fadeUp 0.3s ease 0.1s both"
  >
    <div class="af-body">
      <div class="af-category">
        <div class="cat-dot" style="background: #c0392b"></div>
        <span style="color: #c0392b; letter-spacing: 0.12em">AI 融资</span>
      </div>
      <div class="af-headline">Anthropic 完成 15 亿美元融资，估值超 400 亿美元</div>
      <div class="af-deck">
        谷歌、亚马逊联合领投，本轮融资将主要用于扩大模型训练基础设施投入。创始人 Dario Amodei
        表示将专注于 Claude 商业化落地与企业服务市场拓展。
      </div>
      <div class="ai-summary" id="sum-featured">
        <div class="ai-summary-label">🤖 AI 关联摘要</div>
        <div id="sum-featured-text">
          此轮融资印证 AI
          基础模型赛道仍处资本热度高峰，但投后估值已远超盈利预期，反映投资人押注"平台级基础设施"的长期逻辑。对你影响：<strong
            >Anthropic API 价格短期不会调整</strong
          >，但竞争压力将推动更多模型提供商降价，你的模型选型策略可以更从容。
        </div>
      </div>
      <div class="article-actions">
        <button
          class="act-btn"
          onclick="
            event.stopPropagation();
            this.classList.toggle('active');
            this.innerHTML = this.classList.contains('active') ? '🔖 已收藏' : '🔖 收藏';
          "
        >
          🔖 收藏
        </button>
        <button
          class="act-btn"
          onclick="
            event.stopPropagation();
            deepSummary(this, 'featured');
          "
        >
          🤖 深度解读
        </button>
        <button class="act-btn" onclick="event.stopPropagation()">↗ 原文</button>
        <div class="act-sep"></div>
        <span style="font-family: 'DM Mono', monospace; font-size: 10px; color: var(--ink3)"
          >36氪 · 2小时前</span
        >
      </div>
    </div>
    <div class="af-image">🚀</div>
  </div>

  <div class="section-divider">
    <div class="sd-line"></div>
    <div class="sd-label">融资动态</div>
    <div class="sd-line"></div>
  </div>

  <!-- REGULAR ARTICLES -->
  <div
    class="article-row"
    @click="openArticle"
    style="animation: fadeUp 0.3s ease 0.15s both"
  >
    <div>
      <div class="ar-cat" style="color: #1a3a5c">● 企业SaaS</div>
      <div class="ar-headline">字节跳动旗下飞书发布「知识库 Pro」，直指企业知识管理细分市场</div>
      <div class="ar-deck">
        新产品支持多模态文件管理、AI
        自动摘要和跨部门知识图谱，定价策略激进，对存量企业客户提供6个月免费迁移期。
      </div>
      <div class="ai-summary" id="sum-1" style="display: none">
        <div class="ai-summary-label">🤖 AI 关联摘要</div>
        <div id="sum-1-text">
          <div class="loading-dots"><span></span><span></span><span></span></div>
        </div>
      </div>
      <div class="ar-meta">
        <span style="color: var(--ink2); font-weight: 500">36氪</span>
        <span>45分钟前</span>
        <span style="color: #c0392b; font-weight: 700">⚠ 直接竞品</span>
      </div>
    </div>
    <div class="ar-thumb">📋</div>
  </div>

  <div
    class="article-row"
    @click="openArticle"
    style="animation: fadeUp 0.3s ease 0.2s both"
  >
    <div>
      <div class="ar-cat" style="color: #c0392b">● AI / 大模型</div>
      <div class="ar-headline">
        红杉中国发布《2026年AI+企业服务投资白皮书》：知识管理赛道进入关键窗口期
      </div>
      <div class="ar-deck">
        报告指出未来18个月是AI企业知识管理赛道的黄金融资窗口，Pre-A至A轮估值倍数有望维持8-12倍ARR，建议创业者加速商业化验证。
      </div>
      <div class="ai-summary" id="sum-2" style="display: none">
        <div class="ai-summary-label">🤖 AI 关联摘要</div>
        <div id="sum-2-text"></div>
      </div>
      <div class="ar-meta">
        <span style="color: var(--ink2); font-weight: 500">红杉中国官网</span>
        <span>3小时前</span>
        <span style="color: #2d6a4f; font-weight: 700">★ 强相关</span>
      </div>
    </div>
    <div class="ar-thumb">📊</div>
  </div>

  <div
    class="article-row"
    @click="openArticle"
    style="animation: fadeUp 0.3s ease 0.25s both"
  >
    <div>
      <div class="ar-cat" style="color: #b5620a">● 政策法规</div>
      <div class="ar-headline">国信办发布生成式AI管理办法修订征求意见稿，新增强制内容标注要求</div>
      <div class="ar-deck">
        修订版要求生成式AI产品对AI生成内容实施强制性水印标注，涉及企业内部部署版本豁免申请条件同步公布，预计对企业级AI工具影响有限。
      </div>
      <div class="ar-meta">
        <span style="color: var(--ink2); font-weight: 500">网信办官网</span>
        <span>5小时前</span>
        <span style="color: #b5620a">合规关注</span>
      </div>
    </div>
    <div class="ar-thumb">📜</div>
  </div>

  <div class="section-divider">
    <div class="sd-line"></div>
    <div class="sd-label">更多资讯</div>
    <div class="sd-line"></div>
  </div>

  <div class="compact-list">
    <div class="cl-item">
      <div class="cl-num">6</div>
      <div class="cl-body">
        <div class="cl-headline">明势资本完成新一期5亿美元基金募集，AI+硬科技方向加大配置</div>
        <div class="cl-meta">TechCrunch · 6小时前</div>
      </div>
      <div class="cl-tag" style="background: var(--forest-dim); color: var(--forest)">融资</div>
    </div>
    <div class="cl-item">
      <div class="cl-num">7</div>
      <div class="cl-body">
        <div class="cl-headline">微软 365 Copilot 中国版正式上线，与飞书、钉钉企业场景直接竞争</div>
        <div class="cl-meta">虎嗅 · 7小时前</div>
      </div>
      <div class="cl-tag" style="background: var(--red-dim); color: var(--red)">竞品</div>
    </div>
    <div class="cl-item">
      <div class="cl-num">8</div>
      <div class="cl-body">
        <div class="cl-headline">OpenAI 发布企业级知识库功能 ChatGPT Edu Pro，支持私有化部署</div>
        <div class="cl-meta">The Verge · 8小时前</div>
      </div>
      <div class="cl-tag" style="background: var(--red-dim); color: var(--red)">竞品</div>
    </div>
    <div class="cl-item">
      <div class="cl-num">9</div>
      <div class="cl-body">
        <div class="cl-headline">
          真格基金宣布今年新增 AI Agent 赛道专项 LP，重点关注 B2B 落地应用
        </div>
        <div class="cl-meta">36氪 · 9小时前</div>
      </div>
      <div class="cl-tag" style="background: var(--navy-dim); color: var(--navy)">投资</div>
    </div>
    <div class="cl-item">
      <div class="cl-num">10</div>
      <div class="cl-body">
        <div class="cl-headline">企业SaaS出海报告：中国知识管理类工具在东南亚市场增速超过400%</div>
        <div class="cl-meta">晚点 LatePost · 今天</div>
      </div>
      <div class="cl-tag" style="background: var(--forest-dim); color: var(--forest)">机会</div>
    </div>
  </div>

  <div class="load-more-row">
    <button class="btn-load" onclick="loadMore(this)">加载更多资讯 ↓</button>
  </div>
</template>

<script setup lang="ts">
import '@/styles/module_newsfeed.scss';

const openArticle = () =>{

}
</script>

<style lang="scss"></style>
