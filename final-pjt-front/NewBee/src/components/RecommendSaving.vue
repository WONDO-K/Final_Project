<template>
  <div>
    <h1>추천 Saving</h1>
    <div v-for="best in recommendProduct.saving">
      <p @click="goSavingDetail(best)">{{ best.saving_product__fin_prdt_nm }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goSavingDetail = (best) => {
  store.getSavingDetail(best.saving_product).then(() => {
    router.push({ name: 'savingDetail', params: { id: best.saving_product } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>