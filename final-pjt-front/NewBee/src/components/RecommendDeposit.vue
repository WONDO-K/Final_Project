<template>
  <div>
    <h1>추천 Deposit</h1>
    <div v-for="best in recommendProduct.deposit">
      <p @click="goDepositDetail(best)">{{ best.deposit_product__fin_prdt_nm }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goDepositDetail = (best) => {
  store.getDepositDetail(best.deposit_product).then(() => {
    router.push({ name: 'depositDetail', params: { id: best.deposit_product }})
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>