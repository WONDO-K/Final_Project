<template>
  <div>
    <SavingsList />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue'
import SavingsList from '@/components/SavingsList.vue'


const store = useCounterStore()

onMounted(() => {
  // if (store.savingsList.length === 0){
    store.getSavingsList()
  // }
})
</script>

<style scoped>

</style>