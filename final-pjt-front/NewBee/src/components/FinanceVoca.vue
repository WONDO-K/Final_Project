<template>
  <div>
    <div class="card text-center border-primary" style="width: 18rem;">
      <div class="card-header fw-bold fs-5">
        오늘의 경제용어
      </div>
      <div class="card-body">
          <p class="fw-bold">{{ ecoWord }}</p>
        <h5 class="card-title"></h5>
        <p class="card-text">
          {{ ecoContent }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue';

const store = useCounterStore()
const ecoWord = store.ecoWord
const ecoContent = store.ecoContent
const isRequest = store.isRequest

onMounted(() => {
  if (isRequest === true){
    store.getEcoWord()
  }
})

</script>

<style scoped>
</style>