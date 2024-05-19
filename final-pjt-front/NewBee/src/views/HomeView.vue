<template>
    <div>
        <BestProductImage />
        <FinanceVoca />
        <ExchangeRate />
    </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import FinanceVoca from '@/components/FinanceVoca.vue'
import BestProductImage from '@/components/BestProductImage.vue'
import ExchangeRate from '@/components/ExchangeRate.vue'

</script>

<style scoped>
</style>