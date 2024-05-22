<template>
  <div>
    <h1>Best Pension</h1>
    <div v-for="best in bestProduct.pension">
      <p @click="goPensionDetail(best)">{{ best.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const bestProduct = store.bestProduct

const goPensionDetail = (best) => {
  store.getPensionDetail(best.id).then(() => {
    router.push({ name: 'pensionDetail', params: { id: best.id } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>