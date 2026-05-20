<template>
  <footer>
    <div class="footer-brand">
      <strong style="color:var(--gold)">{{$t('corp_logo_title')}}</strong>
      <span > · {{$t('corp_name')}}</span>
    </div>
    <div class="footer-legal">
      <span > {{$t('corp_copy_right')}}</span>
    </div>
  </footer>
</template>

<script setup  lang="ts">

</script>

<style scoped>
footer {
  padding: 40px 5vw;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  background-color: var(--ink);
}

.footer-brand {
  font-family: var(--serif);
  font-size: 13px;
  color: var(--muted);
}

.footer-legal {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  color: var(--muted2);
  text-transform: uppercase;
}
</style>
