<template>
  <div class="text-center container">
    <div class="d-flex justify-content-between mb-4">
      <BestDeposit />
      <RecommendDeposit v-if="store.isLogin" />
    </div>
    <DepositList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import DepositList from '@/components/DepositList.vue'
import BestDeposit from '@/components/BestDeposit.vue'
import RecommendDeposit from '@/components/RecommendDeposit.vue'

const store = useCounterStore()

onMounted(() => {
  store.getDepositList()
  // store.getBestProduct()
  // store.getRecommendProduct()
})
</script>

<style scoped>
/* 필요한 추가 스타일을 여기에 작성하세요 */
</style>
