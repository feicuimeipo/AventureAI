<template>
  <button class="lang-btn" @click="toggleLanguage" >{{ $t('switch_language')}}</button>
</template>

<script setup lang="ts" >
import {setLocale} from "@/i18n";
import {defineEmits} from "vue";
import {useI18n} from "vue-i18n";
const {locale } = useI18n()

// 1. 定义要抛出的事件名
const emit = defineEmits(['changeEvent'])

const toggleLanguage = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  setLocale(locale.value)
  emit('changeEvent')
}

</script>

<style scoped lang="scss">

.lang-btn {
  font-size: var(--font-size-base);
  letter-spacing: 0.12em;
  padding: 5px;
  border-radius: 2px;
  cursor: pointer !important;
  transition: all 0.2s;
}

.module-partner{
  .lang-btn {
    color: var(--teal);
    background: var(--teal-dim);
    border: 1px solid var(--teal);
  }
}

.module-default{
  .lang-btn {
    color: var(--gold);
    background: var(--gold-dim);
    border: 1px solid var(--gold-line);
  }
}

.module-newsfeed{
  .lang-btn {
    color: var(--ink);
    background: var(--ink3);
    border: 1px solid var(--ink);
  }
}

.module-token{
  .lang-btn {
    color: var(--gold);
    background: var(--gold-dim);
    border: 1px solid var(--gold);
  }
}

.module-platform{
  .lang-btn {
    color: var(--gold);
    background: var(--gold-dim);
    border: 1px solid var(--gold);
  }
}




</style>
