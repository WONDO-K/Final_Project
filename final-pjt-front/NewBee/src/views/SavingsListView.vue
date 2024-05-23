<template>
  <div class="text-center container">
    <div class="d-flex justify-content-between mb-4">
      <BestSaving />
      <RecommendSaving v-if="store.isLogin" />
    </div>
    <SavingsList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue'
import SavingsList from '@/components/SavingsList.vue'
import RecommendSaving from '@/components/RecommendSaving.vue'
import BestSaving from '@/components/BestSaving.vue'

const store = useCounterStore()

onMounted(() => {
  store.getBestProduct()
  // if (store.savingsList.length === 0){
    store.getSavingsList()
    // store.getRecommendProduct()
  // }
})
</script>

<style scoped>

</style>