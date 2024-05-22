<template>
  <div>
    <RecommendSaving />
    <SavingsList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue'
import SavingsList from '@/components/SavingsList.vue'
import RecommendSaving from '@/components/RecommendSaving.vue'

const store = useCounterStore()

onMounted(() => {
  // if (store.savingsList.length === 0){
    store.getSavingsList()
    store.getRecommendProduct()

  // }
})
</script>

<style scoped>

</style>