<template>
  <div>
    <BestLoan />
    <RecommendLoan />
    <LoanList />
  </div>
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
})
</script>

<style scoped>
</style>