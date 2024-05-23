<template>
  <div class="ms-3 mt-3 rounded-3">
    <router-link :to="{ name : 'home' }"><img src="@/assets/images/logo.png" class="rounded-3" alt="logo"></router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
/* 임시 css -> 차후 부트스트랩으로 변경 및 수정 예정 */
img {
  width: 130px;
  height: 130px;
}
</style>