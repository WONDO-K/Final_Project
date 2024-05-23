<template>
  <div class="text-center container">
    <div class="d-flex justify-content-between mb-4">
      <BestLoan />
      <RecommendLoan v-if="store.isLogin" />
    </div>
  </div>
  <LoanList />
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import LoanList from '@/components/LoanList.vue'
import { onMounted } from 'vue'
import BestLoan from '@/components/BestLoan.vue'
import RecommendLoan from '@/components/RecommendLoan.vue'

const store = useCounterStore()

onMounted(() => {
  store.getLoanList()
  store.getBestProduct()
})
</script>

<style scoped>
</style>