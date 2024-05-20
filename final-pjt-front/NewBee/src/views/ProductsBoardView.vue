<template>
  <div>
    <h1>예금 상품 목록</h1>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue'

const store = useCounterStore()

onMounted(
  store.getDepositList()
)

</script>

<style scoped>
</style>