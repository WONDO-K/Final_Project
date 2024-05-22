<template>
  <div>
    <RecommendPension />
    <PensionList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import PensionList from '@/components/PensionList.vue'
import { onMounted } from 'vue'
import RecommendPension from '@/components/RecommendPension.vue'

const store = useCounterStore()

onMounted(() => {
  store.getPensionList()
  store.getRecommendProduct()
})
</script>

<style scoped>
</style>