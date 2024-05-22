<template>
  <div>
    <BestDeposit />
    <RecommendDeposit />
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
  store.getBestProduct()
  store.getRecommendProduct()
})
</script>

<style scoped>
</style>