<template>
  <!-- PURCHASE MODAL -->

  <!--  内容区-->
  <div class="bm-plans">
    <div class="bm-plan" @click="selectPlan(this,200)" data-tokens="200">
      <div class="bp-left">
        <div class="bp-name">基础包</div>
        <div class="bp-tokens">200 Token</div>
      </div>
      <div class="bp-price">¥9.9</div>
    </div>
    <div class="bm-plan on" onclick="selectPlan(this,500)" data-tokens="500">
      <div class="bp-left">
        <div class="bp-name">标准包 ⭐ 推荐</div>
        <div class="bp-tokens">500 Token</div>
        <div class="bp-bonus">限时送 50 Token</div>
      </div>
      <div class="bp-price">¥19.9</div>
    </div>
    <div class="bm-plan" @click="selectPlan(this,1500)" data-tokens="1500">
      <div class="bp-left">
        <div class="bp-name">年度包</div>
        <div class="bp-tokens">1500 Token</div>
        <div class="bp-bonus">赠送 500 Token</div>
      </div>
      <div class="bp-price">¥49.9</div>
    </div>
  </div>
  <button type="button" class="btn btn-primary"   @click="doBuy">立即购买</button>


</template>

<script setup lang="ts">
import {defineEmits} from "vue";
import {showBootStrapToast} from "@/views/token/ToastForToken.tsx";

const emit = defineEmits(['saveDataSuccess','closeBuyDialog','updateDisplay','updateBalance'])


let selectedPlan = { tokens: 500 };
function selectPlan(el, tokens) {
  document.querySelectorAll('.bm-plan').forEach(p => p.classList.remove('on'));
  el.classList.add('on');
  selectedPlan = { tokens };
}


const doBuy = () =>{
  const bonus = selectedPlan.tokens >= 1500 ? 500 : selectedPlan.tokens >= 500 ? 50 : 0;
  const total = selectedPlan.tokens + bonus;


  emit('updateBalance',total)
  emit('updateDisplay');
  //do
  emit("closeBuyDialog")
  showBootStrapToast("💎","充值成功！"+total + "Token",bonus > 0 ? "含赠送"+bonus:"已到账",true)
  emit("saveDataSuccess",total,bonus)
}



</script>

<style scoped>

</style>
