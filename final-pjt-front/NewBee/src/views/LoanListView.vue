<template>
  <div>
    <LoanList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import LoanList from '@/components/LoanList.vue'
import { onMounted } from 'vue'

const store = useCounterStore()

onMounted(() => {
  store.getLoanList()
})
</script>

<style scoped>
</style>