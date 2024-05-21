<template>
  <div>
    <DepositList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import DepositList from '@/components/DepositList.vue'

const store = useCounterStore()

onMounted(() => {
  if (store.depositList.length === 0){
    store.getDepositList()
  }
})
</script>

<style scoped>
</style>