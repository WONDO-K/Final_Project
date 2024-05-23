<template>
  <div class="text-center container">
    <div class="d-flex justify-content-between mb-4">
      <BestPension />
      <RecommendPension v-if="store.isLogin"/>
    </div>
    <PensionList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import PensionList from '@/components/PensionList.vue'
import { onMounted } from 'vue'
import RecommendPension from '@/components/RecommendPension.vue'
import BestPension from '@/components/BestPension.vue'

const store = useCounterStore()

onMounted(() => {
  store.getPensionList()
  store.getBestProduct()
  // store.getRecommendProduct()
})
</script>

<style scoped>
</style>