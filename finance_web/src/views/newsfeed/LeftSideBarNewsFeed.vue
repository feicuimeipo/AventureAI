<template>

  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">我的订阅</div>
      <div class="wh-more" onclick="openSubscribeWidget()">管理</div>
    </div>
    <div class="sub-list">
      <div class="sub-item active">
        <div class="sub-dot" style="background:#c0392b"></div>
        <div class="sub-name">AI / 大模型</div>
        <div class="sub-count">12</div>
      </div>
      <div class="sub-item active">
        <div class="sub-dot" style="background:#1a3a5c"></div>
        <div class="sub-name">企业 SaaS</div>
        <div class="sub-count">8</div>
      </div>
      <div class="sub-item">
        <div class="sub-dot" style="background:#2d6a4f"></div>
        <div class="sub-name">融资动态</div>
        <div class="sub-count">5</div>
      </div>
      <div class="sub-item">
        <div class="sub-dot" style="background:#b5620a"></div>
        <div class="sub-name">政策法规</div>
        <div class="sub-count">3</div>
      </div>
      <div class="sub-item">
        <div class="sub-dot" style="background:#5b3d8a"></div>
        <div class="sub-name">产品发布</div>
        <div class="sub-count">6</div>
      </div>
    </div>
  </div>

  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">今日热词</div>
    </div>
    <div class="trend-list">
      <div class="trend-item"><div class="trend-num">1</div><div class="trend-text"><strong>DeepSeek V3</strong>开源发布引发全球热议</div></div>
      <div class="trend-item"><div class="trend-num">2</div><div class="trend-text"><strong>AI监管新规</strong>欧盟AI法案正式生效</div></div>
      <div class="trend-item"><div class="trend-num">3</div><div class="trend-text"><strong>字节系SaaS</strong>企业市场大规模扩张</div></div>
      <div class="trend-item"><div class="trend-num">4</div><div class="trend-text"><strong>Anthropic</strong>获新一轮15亿美元融资</div></div>
      <div class="trend-item"><div class="trend-num">5</div><div class="trend-text"><strong>AI Agent</strong>商业化加速，多家机构出手</div></div>
    </div>
  </div>

  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">关注公司动态</div>
      <div class="wh-more">添加</div>
    </div>
    <div class="tracker-list">
      <div class="tracker-item">
        <div class="tracker-name">字节跳动</div>
        <div class="tracker-change tc-up">+3条新闻</div>
      </div>
      <div class="tracker-item">
        <div class="tracker-name">Anthropic</div>
        <div class="tracker-change tc-up">+2条新闻</div>
      </div>
      <div class="tracker-item">
        <div class="tracker-name">红杉中国</div>
        <div class="tracker-change tc-up">+1条新闻</div>
      </div>
      <div class="tracker-item">
        <div class="tracker-name">阿里云</div>
        <div class="tracker-change tc-flat">暂无更新</div>
      </div>
      <div class="tracker-item">
        <div class="tracker-name">飞书</div>
        <div class="tracker-change tc-down">1条竞品动态</div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">

</style>
