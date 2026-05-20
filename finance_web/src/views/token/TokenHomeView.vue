<template>
  <!-- PURCHASE MODAL -->
  <div class="modal-overlay fade" id="buyModal" :class="{ show: showBuyModal }" v-if="showBuyModal" tabindex="-1" aria-modal="true" role="dialog">
    <div class="modal-dialog">
      <div class="buy-modal">
        <div class="bm-header">
          <div class="bm-title">💎 购买 Token 包</div>
          <div class="bm-close" @click="closeBuyDialog">✕</div>
        </div>
        <div class="bm-body">
            <PurchaseModal @saveDataSuccess="handleCloseBuyModal" @closeBuyDialog="closeBuyDialog" @updateBalance="updateBalance" @updateDisplay="updateDisplay" />
        </div>
      </div>
    </div>
  </div>

  <!-- TOKEN HERO -->
  <div class="token-hero">
    <div class="th-bg">TOKEN</div>
    <div class="th-eyebrow">CURRENT BALANCE · 当前余额</div>
    <div class="th-amount">
      <div class="th-num" id="heroBalance">1,840</div>
      <div class="th-unit">Token</div>
    </div>
    <div class="th-sub">今日已获得 <span id="todayEarned">+45</span> Token · 连续登录 48 天</div>
    <div class="th-actions">
      <button class="th-btn th-btn-primary" @click="openBuyDialog">💎 购买 Token</button>
      <button class="th-btn th-btn-secondary" @click="showToast('📜','查看兑换记录','功能开发中',false)">📜 消耗记录</button>
      <button class="th-btn th-btn-secondary" @click="dailyCheckIn()">✅ 每日签到</button>
      <button class="th-btn th-btn-secondary" @click="showToast('📨','邀请好友','每成功邀请一位好友 +100T',true)">📨 邀请 +100T</button>
    </div>
    <!-- MINI CHART -->
    <div class="th-history">
      <div class="thh-label">近 14 天 Token 变化</div>
      <div class="thh-bars" id="miniChart"></div>
    </div>
  </div>

  <!-- DAILY TASKS -->
  <div>
    <div class="section-header">
      <div>
        <div class="sh-title">📋 今日任务</div>
        <div class="sh-sub">完成任务获得 Token 奖励</div>
      </div>
      <div class="sh-action" @click="showToast('📋','任务历史','可以查看所有历史任务完成记录',false)">历史记录</div>
    </div>
    <div class="task-grid" id="taskGrid">

      <div class="task-card done" id="task-checkin">
        <div class="tc-cat" style="background:var(--green-dim);color:var(--green);">每日</div>
        <div class="tc-icon">✅</div>
        <div class="tc-name">每日签到</div>
        <div class="tc-desc">每天登录平台完成签到，连续签到额外奖励</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +5</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:100%"></div></div>
            <div class="tc-prog-label">1/1</div>
          </div>
        </div>
      </div>

      <div class="task-card" id="taskCardReadNews" @click="completeTask('taskCardReadNews','阅读3篇行业资讯',20)">
        <div class="tc-cat blue">信息流</div>
        <div class="tc-icon">📰</div>
        <div class="tc-name">阅读行业资讯</div>
        <div class="tc-desc">今日已阅读 2 篇行业资讯，再读 1 篇完成任务</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +20</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:66%"></div></div>
            <div class="tc-prog-label">2/3</div>
          </div>
        </div>
      </div>

      <div class="task-card" id="taskCardMatchingInvestor" @click="completeTask('taskCardMatchingInvestor','完成一次投资人匹配',30)">
        <div class="tc-cat purple">匹配</div>
        <div class="tc-icon">🎯</div>
        <div class="tc-name">查看投资人匹配</div>
        <div class="tc-desc">进入模块三，查看今日为你匹配的投资人列表</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +30</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:0%"></div></div>
            <div class="tc-prog-label">0/1</div>
          </div>
        </div>
      </div>

      <div class="task-card" id="taskcardPostComment" @click="completeTask('taskcardPostComment','发表一条评论',15)">
        <div class="tc-cat orange">社区</div>
        <div class="tc-icon">💬</div>
        <div class="tc-name">参与社区讨论</div>
        <div class="tc-desc">在行业资讯下发表你的观点，与同行交流</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +15</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:0%"></div></div>
            <div class="tc-prog-label">0/1</div>
          </div>
        </div>
      </div>

      <div class="task-card" id="taskCardUpdatePBDocument" @click="completeTask('taskCardUpdatePBDocument','更新BP文档',25)">
        <div class="tc-cat gold4" >融资</div>
        <div class="tc-icon">📄</div>
        <div class="tc-name">优化商业计划书</div>
        <div class="tc-desc">使用AI编辑器优化至少一个BP章节</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +25</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:0%"></div></div>
            <div class="tc-prog-label">0/1</div>
          </div>
        </div>
      </div>

      <div class="task-card"  id="taskCardFollowFounder" @click="completeTask('taskCardFollowFounder','关注一位创业者',10)">
        <div class="tc-cat" style="background:var(--green-dim);color:var(--green);">社交</div>
        <div class="tc-icon">👋</div>
        <div class="tc-name">加好友建立连接</div>
        <div class="tc-desc">关注一位同赛道的创业者或投资人</div>
        <div class="tc-footer">
          <div class="tc-reward">🪙 +10</div>
          <div class="tc-progress">
            <div class="tc-prog-bar"><div class="tc-prog-fill" style="width:0%"></div></div>
            <div class="tc-prog-label">0/1</div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- WEEKLY CHALLENGE -->
  <div>
    <div class="section-header">
      <div class="sh-title">⚡ 本周挑战</div>
    </div>
    <div class="challenge-card">
      <div class="cc-left">
        <div class="cc-eyebrow">WEEKLY CHALLENGE · 截止周日 23:59</div>
        <div class="cc-title">发送 BP 给 3 位匹配投资人</div>
        <div class="cc-desc">本周已向王兴远发送定制BP，还需再向 2 位投资人发送，完成后获得大额 Token 奖励。</div>
        <div class="cc-progress">
          <div class="cc-bar-wrap">
            <div class="cc-bar-fill" id="challengeBar" style="width:33%"></div>
          </div>
          <div class="cc-pct" id="challengePct">33%</div>
        </div>
      </div>
      <div class="cc-right">
        <div class="cc-reward-label">完成奖励</div>
        <div class="cc-reward-val">+200</div>
        <div class="cc-reward-unit">Token</div>
        <div class="cc-time">剩余 4 天 18 小时</div>
      </div>
    </div>
  </div>

  <!-- TRANSACTION HISTORY -->
  <div>
    <div class="section-header">
      <div class="sh-title">📊 Token 流水</div>
      <div class="sh-action">全部记录</div>
    </div>
    <div class="history-table">
      <div class="ht-head">
        <div class="ht-cell">操作</div>
        <div class="ht-cell">类型</div>
        <div class="ht-cell">数量</div>
        <div class="ht-cell">时间</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon green" >✅</div>
          <div><div class="ht-desc-text">每日签到</div><div class="ht-desc-sub">连续第48天 · +5</div></div>
        </div>
        <div><div class="ht-type green" >签到</div></div>
        <div class="ht-amount earn">+5</div>
        <div class="ht-date">今天 07:02</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon red">✏️</div>
          <div><div class="ht-desc-text">AI重写BP第二节</div><div class="ht-desc-sub">智链SaaS · 模块三</div></div>
        </div>
        <div><div class="ht-type red" >消耗</div></div>
        <div class="ht-amount spend">-20</div>
        <div class="ht-date">今天 10:34</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon green">📰</div>
          <div><div class="ht-desc-text">阅读行业资讯（2篇）</div><div class="ht-desc-sub">今日任务进度 2/3</div></div>
        </div>
        <div><div class="ht-type green">任务</div></div>
        <div class="ht-amount earn">+10</div>
        <div class="ht-date">今天 09:18</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon red" >📤</div>
          <div><div class="ht-desc-text">向王兴远发送定制BP</div><div class="ht-desc-sub">红杉中国 · 融资管道</div></div>
        </div>
        <div><div class="ht-type red">消耗</div></div>
        <div class="ht-amount spend">-30</div>
        <div class="ht-date">昨天 16:45</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon blue" >👥</div>
          <div><div class="ht-desc-text">成功邀请新用户注册</div><div class="ht-desc-sub">陈晓婷 · 被邀请人已完善档案</div></div>
        </div>
        <div><div class="ht-type blue" >邀请</div></div>
        <div class="ht-amount earn">+100</div>
        <div class="ht-date">3天前</div>
      </div>

      <div class="ht-row">
        <div class="ht-desc">
          <div class="ht-desc-icon glod" >💎</div>
          <div><div class="ht-desc-text">购买 Token 包（标准包）</div><div class="ht-desc-sub">支付宝 · 订单号 PAY20260301</div></div>
        </div>
        <div><div class="ht-type glod">充值</div></div>
        <div class="ht-amount earn">+550</div>
        <div class="ht-date">5天前</div>
      </div>
    </div>
  </div>

    <!-- 整个模态框 -->




</template>

<script setup lang="ts">
import {ref} from 'vue'
import PurchaseModal from "@/views/token/PurchaseModal.vue";
import {showBootStrapToast} from "@/views/token/ToastForToken.tsx"; // 确保你已经正确引入了Bootstrap的JS部分


const showBuyModal = ref<boolean>(false);
const openBuyDialog = () => {
  showBuyModal.value = true;
}

const closeBuyDialog =() =>{
  console.log("关闭模式")
  showBuyModal.value = false;
}

const handleCloseBuyModal = (total:number, bonues:number) => {
  console.log("购买成功!")
}



let balance = 1840;
let todayEarned = 45;
let checkedIn = false;
function dailyCheckIn() {
  if (checkedIn) { showToast('✅','今日已签到','明天再来可继续获得奖励',false); return; }
  checkedIn = true;
  balance += 5;
  todayEarned += 5;
  updateDisplay();
  showToast('✅','连续签到第 49 天！','明天签到解锁额外 +50T 周奖励',true);
}

// Spend token
function spendToken(btn, cost, name) {
  if (balance < cost) {
    showToast('❌','Token不足',`需要 ${cost}T，当前 ${balance}T`,false);
    openBuyDialog();
    return;
  }
  balance -= cost;
  updateDisplay();
  btn.textContent = '✓ 已兑换';
  btn.classList.add('bought');
  showToast('✨', `已兑换：${name}`, `-${cost} Token`, false);
}




const showToast = async (icon: string,
                         text: string,
                         change: string,
                         isPositive: boolean) => {
  await showBootStrapToast(icon, text, change, isPositive);
}

const completeTask = (id:string, taskName:string,reward:number) =>{
  const el = document.getElementById(id);
  if (el.classList.contains('done')) return;
  el.classList.add('done');
  // Update progress bar
  const fill = el.querySelector('.tc-prog-fill');
  const label = el.querySelector('.tc-prog-label');
  if (fill) fill.style.width = '100%';
  if (label) label.textContent = '1/1';

  balance += reward;
  todayEarned += reward;
  updateDisplay();

  showToast('🪙', `完成：${taskName}`, `+${reward} Token 已到账`, true);
}

// Update display
function updateDisplay() {
  const fmt = n => n.toLocaleString();
  document.getElementById('navBalance').textContent = fmt(balance);
  document.getElementById('heroBalance').textContent = fmt(balance);
  document.getElementById('lbMyTokens').textContent = fmt(balance);
  document.getElementById('navChange').textContent = '+今日 ' + todayEarned;
  document.getElementById('todayEarned').textContent = '+' + todayEarned;

  // Level progress
  const lvMin = 2000, lvMax = 5000;
  const pct = Math.min(100, Math.round(((balance - lvMin) / (lvMax - lvMin)) * 100));
  document.getElementById('lpFill').style.width = Math.max(0,pct) + '%';
  document.getElementById('lpText').textContent = `${fmt(balance)} / ${fmt(lvMax)}`;
}

function updateBalance(total:number){
  balance += total;
}

function updateMimiChart(){
// Build mini chart
  const chartData = [120,80,200,150,320,90,180,260,140,380,210,290,180,420];
  const maxVal = Math.max(...chartData);
  const chartEl = document.getElementById('miniChart');
  chartData.forEach((v,i) => {
    const bar = document.createElement('div');
    bar.className = 'thh-bar';
    const h = Math.max(6, (v/maxVal)*40);
    bar.style.height = h + 'px';
    const isToday = i === chartData.length - 1;
    bar.style.background = isToday
        ? 'linear-gradient(180deg,var(--gold),var(--gold2))'
        : v > 200 ? 'rgba(79,142,247,0.4)' : 'rgba(255,255,255,0.08)';
    bar.title = (i === chartData.length-1 ? '今天' : `${14-i}天前`) + ' +' + v + 'T';
    chartEl.appendChild(bar);
  });

}

// updateDisplay()
// updateMimiChart()
</script>

<style scoped>

</style>
