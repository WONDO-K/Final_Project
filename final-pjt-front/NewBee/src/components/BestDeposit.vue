<template>
  <div>
    <h1>Best Deposit</h1>
    <div v-for="best in bestProduct.deposit">
      <p @click="goDepositDetail(best)">{{ best.name }}</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router';
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const bestProduct = store.bestProduct

const goDepositDetail = (best) => {
  store.getDepositDetail(best.id).then(() => {
    router.push({ name: 'depositDetail', params: { id: best.id } })
  })
}
</script>

<style scoped>
p.hover {
  cursor: pointer;
}

</style>