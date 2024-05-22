<template>
  <div>
    <h1>Best Pension</h1>
    <div v-for="best in bestProduct.rent_loan">
      <p @click="goLoanDetail(best)">{{ best.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const bestProduct = store.bestProduct

const goLoanDetail = (best) => {
  store.getLoanDetail(best.id).then(() => {
    router.push({ name: 'loanDetail', params: { id: best.id } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>