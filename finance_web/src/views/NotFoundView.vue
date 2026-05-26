
<script setup lang="ts">
import ReturnHome from '@/components/BtnReturnHome.vue';
import ReturnPrevious from '@/components/BtnReturnPrevious.vue';
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br flex items-center justify-center p-10 " >
    <div class="max-w-2xl text-center" >
      <div style="display: inline-block">
        <svg class="w-40 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z">
          </path>
        </svg><br/>
        <h1 class="text-5xl font-bold text-yellow-500 mb-4">404</h1>
      </div>
      <br><br>
      <h2 class="text-2xl text-yellow-500 text-gray-800 mb-6">页面未找到</h2>
      <br>
      <p class="text-gray-500 mb-10 max-w-xl mx-auto text-center" style="font-size: 18px !important;">抱歉，您访问的页面不存在，请检查您输入的地址。
      </p>
      <div class="flex flex-col sm:flex-row justify-center gap-4" style="margin:10px;font-size: 16px !important;">
          <ReturnHome />
          <return-previous />
      </div>

    </div>
  </div>
</template>
