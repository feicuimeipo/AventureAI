<template>
  <!-- SHOP -->
  <div class="shop-card">
    <div class="widget-head" style="padding:12px 14px;">
      <div class="wh-title">🛒 Token 兑换商城</div>
    </div>
    <div class="shop-tabs">
      <div class="shop-tab on" id="tablabel_service" @click="setShopTab('service')">平台服务</div>
      <div class="shop-tab" id="tablabel_privilege" @click="setShopTab('privilege')">专属权益</div>
      <div class="shop-tab" id="tablabel_cash" @click="setShopTab('cash')">提现兑现</div>
    </div>

    <!-- SERVICE TAB -->
    <div id="tab-service">
      <div class="shop-item">
        <div class="si-icon gold4">✨</div>
        <div class="si-body">
          <div class="si-name">AI深度解读 <span class="si-badge orange">HOT</span></div>
          <div class="si-desc">单篇文章深度AI关联分析，针对你的项目生成洞察</div>
          <div class="si-footer">
            <div class="si-price">🪙 20 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,20,'AI深度解读')">兑换</button>
          </div>
        </div>
      </div>
      <div class="shop-item">
        <div class="si-icon blue" >🎯</div>
        <div class="si-body">
          <div class="si-name">投资人精准匹配报告</div>
          <div class="si-desc">生成针对特定投资人的完整分析报告，含历史案例对比</div>
          <div class="si-footer">
            <div class="si-price">🪙 50 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,50,'投资人匹配报告')">兑换</button>
          </div>
        </div>
      </div>
      <div class="shop-item">
        <div class="si-icon purple" >🌍</div>
        <div class="si-body">
          <div class="si-name">BP 英文版生成</div>
          <div class="si-desc">将完整商业计划书翻译并本地化为专业英文版本</div>
          <div class="si-footer">
            <div class="si-price">🪙 40 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,40,'BP英文版')">兑换</button>
          </div>
        </div>
      </div>
    </div>

    <!-- PRIVILEGE TAB -->
    <div id="tab-privilege" style="display:none">
      <div class="shop-item">
        <div class="si-icon gold4" >👑</div>
        <div class="si-body">
          <div class="si-name">置顶展示 7 天</div>
          <div class="si-desc">在投资人搜索结果中置顶显示你的项目，提升曝光率</div>
          <div class="si-footer">
            <div class="si-price">🪙 200 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,200,'置顶展示7天')">兑换</button>
          </div>
        </div>
      </div>
      <div class="shop-item">
        <div class="si-icon" style="background:var(--blue-dim);">📩</div>
        <div class="si-body">
          <div class="si-name">投资人邮件直送</div>
          <div class="si-desc">绕过平台消息，直接发送到指定投资人企业邮箱</div>
          <div class="si-footer">
            <div class="si-price">🪙 150 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,150,'邮件直送')">兑换</button>
          </div>
        </div>
      </div>
      <div class="shop-item">
        <div class="si-icon green" >🔓</div>
        <div class="si-body">
          <div class="si-name">解锁投资人联系方式</div>
          <div class="si-desc">查看已认证投资人的直接微信/邮箱联系方式</div>
          <div class="si-footer">
            <div class="si-price">🪙 80 <span>Token</span></div>
            <button class="si-buy" @click="spendToken(this,80,'联系方式')">兑换</button>
          </div>
        </div>
      </div>
    </div>

    <!-- CASH TAB -->
    <div id="tab-cash" style="display:none">
      <div style="padding:20px;text-align:center;">
        <div style="font-size:32px;margin-bottom:10px;">💸</div>
        <div class="cash_token_label">Token 兑现</div>
        <div class="cash_token_desc">
          认证合伙人（LV.3）及以上可将 Token 兑换为现金红包或专属服务券。汇率：<strong class="cash_token_value">1000T = ¥50</strong>
        </div>
        <div class="cash_token_cashable_bg">
          <div class="cash_token_cashable_label">当前可兑换</div>
          <div class="cash_token_cashable_value_1">¥ 92.00</div>
          <div class="cash_token_cashable_value_2">= 1,840 Token</div>
        </div>
        <button class="btn_apply_withdraw_cash" @click="showToast('💸','申请提现','功能开发中，升级LV.4后开放',false)">申请提现</button>
      </div>
    </div>
  </div>

  <!-- LEADERBOARD -->
  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">🏅 本月排行榜</div>
      <div class="wh-more">完整榜单</div>
    </div>
    <div class="lb-list">
      <div class="lb-item">
        <div class="lb-rank r1">1</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#f0c040,#e8a020);">王</div>
        <div class="lb-info">
          <div class="lb-name">王建国</div>
          <div class="lb-role">AI · Series A</div>
        </div>
        <div class="lb-tokens">8,420</div>
      </div>
      <div class="lb-item">
        <div class="lb-rank r2">2</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#9ba3b8,#6c7390);">刘</div>
        <div class="lb-info">
          <div class="lb-name">刘晓雨</div>
          <div class="lb-role">医疗AI · Pre-A</div>
        </div>
        <div class="lb-tokens">6,890</div>
      </div>
      <div class="lb-item">
        <div class="lb-rank r3">3</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#f59e0b,#d97706);">陈</div>
        <div class="lb-info">
          <div class="lb-name">陈明磊</div>
          <div class="lb-role">企业SaaS · A</div>
        </div>
        <div class="lb-tokens">5,340</div>
      </div>
      <div class="lb-item">
        <div class="lb-rank">4</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);">孟</div>
        <div class="lb-info">
          <div class="lb-name">孟思远</div>
          <div class="lb-role">机器人 · 天使</div>
        </div>
        <div class="lb-tokens">3,780</div>
      </div>
      <div class="lb-item me">
        <div class="lb-rank">6</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#4f8ef7,#a78bfa);">张</div>
        <div class="lb-info">
          <div class="lb-name">张明远 <span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--gold);">· 我</span></div>
          <div class="lb-role">AI SaaS · Pre-A</div>
        </div>
        <div class="lb-tokens" id="lbMyTokens">1,840</div>
      </div>
      <div class="lb-item">
        <div class="lb-rank">7</div>
        <div class="lb-av" style="background:linear-gradient(135deg,#3ecf8e,#059669);">赵</div>
        <div class="lb-info">
          <div class="lb-name">赵子轩</div>
          <div class="lb-role">新能源 · 天使</div>
        </div>
        <div class="lb-tokens">1,620</div>
      </div>
    </div>
  </div>

  <!-- GROWTH PATH -->
  <div class="widget">
    <div class="widget-head">
      <div class="wh-title">📈 成长路径</div>
    </div>
    <div style="padding:12px 14px;display:flex;flex-direction:column;gap:8px;">
      <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:var(--bg3);">
        <div style="font-size:16px;">🌱</div>
        <div style="flex:1;">
          <div style="font-size:11px;color:var(--text3);">LV.1 新芽</div>
          <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;">0 – 499T</div>
        </div>
        <div style="font-size:10px;color:var(--green);">✓ 已解锁</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:var(--bg3);">
        <div style="font-size:16px;">⚡</div>
        <div style="flex:1;">
          <div style="font-size:11px;color:var(--text3);">LV.2 活跃者</div>
          <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;">500 – 1999T</div>
        </div>
        <div style="font-size:10px;color:var(--green);">✓ 已解锁</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:var(--gold4);border:1px solid rgba(240,192,64,0.2);">
        <div style="font-size:16px;">🤝</div>
        <div style="flex:1;">
          <div style="font-size:11px;color:var(--gold);font-weight:600;">LV.3 认证合伙人 ← 当前</div>
          <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;">2000 – 4999T</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:var(--bg3);opacity:0.6;">
        <div style="font-size:16px;">🔥</div>
        <div style="flex:1;">
          <div style="font-size:11px;color:var(--text);">LV.4 核心贡献者</div>
          <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;">5000 – 19999T · 还差 160T</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:var(--bg3);opacity:0.4;">
        <div style="font-size:16px;">👑</div>
        <div style="flex:1;">
          <div style="font-size:11px;color:var(--text);">LV.5 平台股东</div>
          <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;">20000T+ · 股改参与资格</div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
// Shop tabs
import {showBootStrapToast} from "@/views/token/ToastForToken.tsx";

function setShopTab(id:string) {
  const tabEl = document.getElementById("tablabel_"+id);
  document.querySelectorAll('.shop-tab').forEach(t => t.classList.remove('on'));
  tabEl.classList.add('on');
  ['service','privilege','cash'].forEach(t => {
    const el = document.getElementById('tab-' + t);
    if (el) el.style.display = t === id ? 'block' : 'none';
  });
}

// Spend token
function spendToken(btn, cost, name) {
  // if (balance < cost) {
  //   showBootStrapToast('❌','Token不足',`需要 ${cost}T，当前 ${balance}T`,false);
  //   openBuyDialog();
  //   return;
  // }
  // balance -= cost;
  // updateDisplay();
  // btn.textContent = '✓ 已兑换';
  // btn.classList.add('bought');
   showBootStrapToast('✨', `已兑换：${name}`, `-${cost} Token`, false);
}

const showToast = async (icon: string,
                         text: string,
                         change: string,
                         isPositive: boolean) => {
  await showBootStrapToast(icon, text, change, isPositive);
}


</script>

<style scoped>

</style>
