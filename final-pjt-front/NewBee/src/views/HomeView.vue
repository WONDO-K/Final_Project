<template>
    <div>
        <BestProductImage />
      <div class="container d-flex justify-content-between">
        <FinanceVoca />
        <News />
        <ExchangeRate />
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