<template>
  <div class="text-center text-align-center">
    <div class="mb-4">
      <BestProductImage />
    </div>
    <div class="container d-flex justify-content-between">
      <FinanceVoca />
      <ExchangeRate />
      <News />
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import FinanceVoca from '@/components/FinanceVoca.vue'
import BestProductImage from '@/components/BestProductImage.vue'
import ExchangeRate from '@/components/ExchangeRate.vue'
import News from '@/components/News.vue'

</script>

<style scoped>
</style>