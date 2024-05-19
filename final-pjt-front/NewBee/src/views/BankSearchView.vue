<template>
  <div class="container text-center">
    <h1 class="mb-4">근처 은행 찾기</h1>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <Map />
      </div>
    </div>
  </div>
</template>

<script setup>
import Map from '@/components/Map.vue'
</script>

<style scoped>
/* 부트스트랩 스타일을 적용하기 때문에 임시 CSS는 필요 없습니다. */
</style>