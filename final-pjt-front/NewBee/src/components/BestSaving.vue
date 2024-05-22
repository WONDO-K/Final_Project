<template>
  <div>
    <h1>Best Saving</h1>
    <div v-for="best in bestProduct.saving">
      <p @click="goSavingDetail(best)">{{ best.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const bestProduct = store.bestProduct

const goSavingDetail = (best) => {
  store.getSavingDetail(best.id).then(() => {
    router.push({ name: 'savingDetail', params: { id: best.id } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}
</style>