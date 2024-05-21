<template>
  <div>
    <PensionList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import PensionList from '@/components/PensionList.vue'
import { onMounted } from 'vue'

const store = useCounterStore()

onMounted(() => {
  if (store.pensionList.length === 0){
    store.getPensionList()
  }
})
</script>

<style scoped>
</style>