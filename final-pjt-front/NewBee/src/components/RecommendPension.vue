<template>
  <div>
    <h1>추천 연금</h1>
    <div v-for="best in recommendProduct.pension">
      <p @click="goPensionDetail(best)">{{ best.pension_product__fin_prdt_nm }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goPensionDetail = (best) => {
  store.getPensionDetail(best.pension_product).then(() => {
    router.push({ name: 'pensionDetail', params: { id: best.pension_product } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>