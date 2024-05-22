<template>
  <div>
    <h1>추천 Pension</h1>
    <div v-for="best in recommendProduct.rent_loan">
      <p @click="goLoanDetail(best)">{{ best.pension_product__fin_prdt_nm }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goLoanDetail = (best) => {
  store.getLoanDetail(best.pension_product).then(() => {
    router.push({ name: 'loanDetail', params: { id: best.pension_product } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>