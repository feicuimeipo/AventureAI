<template>
  <!-- ═══ VIEW: MESSAGES ═══ -->
  <div class="view" id="view-messages">
    <div class="msg-layout">
      <!-- Conversation List -->
      <div class="conversations">
        <div class="conv-header">
          <div class="conv-header-title">消息</div>
          <div class="conv-search">
            <span style="color: var(--muted)">🔍</span>
            <input placeholder="搜索对话…" />
          </div>
        </div>
        <div class="conv-list">
          <div class="conv-item active">
            <div class="conv-av" style="background: var(--teal-light); color: var(--teal)">陈</div>
            <div class="conv-body">
              <div style="display: flex; justify-content: space-between; align-items: center">
                <div class="conv-name">陈晓婷</div>
                <div class="conv-time">14:38</div>
              </div>
              <div class="conv-preview">好的，明天下午3点方便视频…</div>
              <div class="match-pill mp-high">匹配度 94</div>
            </div>
          </div>
          <div class="conv-item">
            <div class="conv-av" style="background: #f0edf9; color: var(--violet)">王</div>
            <div class="conv-body">
              <div style="display: flex; justify-content: space-between; align-items: center">
                <div class="conv-name">王子睿</div>
                <div class="conv-badge">2</div>
              </div>
              <div class="conv-preview">你们目前的商业化路径是怎么…</div>
              <div class="match-pill mp-high">匹配度 88</div>
            </div>
          </div>
          <div class="conv-item">
            <div class="conv-av" style="background: #fdf3e7; color: var(--amber)">吴</div>
            <div class="conv-body">
              <div style="display: flex; justify-content: space-between; align-items: center">
                <div class="conv-name">吴晨光</div>
                <div class="conv-time">昨天</div>
              </div>
              <div class="conv-preview">我在 SaaS 销售方面有比较多经验…</div>
              <div class="match-pill" style="background: var(--amber-light); color: var(--amber)">
                匹配度 85
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat -->
      <div class="chat-area">
        <div class="chat-header">
          <div class="chat-header-av" style="background: var(--teal-light)">陈</div>
          <div>
            <div class="chat-header-name">陈晓婷</div>
            <div class="chat-header-status">● 在线 · 匹配度 94</div>
          </div>
          <div class="chat-header-actions">
            <button class="chat-action-btn">查看档案</button>
            <button class="chat-action-btn primary">📅 约一个时间</button>
          </div>
        </div>

        <div class="chat-messages">
          <div class="sys-msg">
            <div class="sys-bubble">🤝 双方互相表达兴趣，私信已解锁 · 2月26日</div>
          </div>

          <div class="msg-group">
            <div class="msg-av" style="background: var(--teal-light); color: var(--teal)">陈</div>
            <div class="msg-bubbles">
              <div class="bubble other">
                你好！看到你的需求，感觉方向挺契合的，我目前也在探索 AI SaaS 的创业机会。
              </div>
              <div class="bubble other">
                能简单介绍一下你们现在项目的阶段和你最需要的技术侧支持是什么吗？
              </div>
              <div class="msg-time">14:15</div>
            </div>
          </div>

          <div class="msg-group own">
            <div class="msg-av" style="background: var(--teal); color: #fff">张</div>
            <div class="msg-bubbles">
              <div class="bubble own">
                你好！我们在做企业内部知识管理的 AI 助手，目前 MVP 已经跑通，有2个种子客户在试用。
              </div>
              <div class="bubble own">
                主要需要一个能 hold 住后端架构和 AI 工程的 CTO，你在字节飞书的经历太对口了。
              </div>
              <div class="msg-time">14:22</div>
            </div>
          </div>

          <div class="msg-group">
            <div class="msg-av" style="background: var(--teal-light); color: var(--teal)">陈</div>
            <div class="msg-bubbles">
              <div class="bubble other">
                好的，明天下午3点方便视频聊吗？我想更深入了解一下产品和技术现状。
              </div>
              <div class="msg-time">14:38</div>
            </div>
          </div>
        </div>

        <div class="chat-input-area">
          <div class="chat-input-wrap">
            <textarea class="chat-input" placeholder="输入消息…" rows="1"></textarea>
            <button class="btn-send-chat">发送</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import '@/styles/module_partner.scss';
import { onMounted } from 'vue';
import { togleElementById } from '@/utils/menuUtils.ts';

onMounted(() => {
  togleElementById('partnerSidebar', false);
});
</script>

<style scoped lang="scss"></style>
