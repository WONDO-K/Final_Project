<template>
  <div>
    <h1>연금 상품 상세 페이지</h1>
    <button @click="joinPension">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const pensionId = route.params.id
const optionId = ref(1)

const joinPension = function(){
  const payload = {
    product_type: '연금',
    product_id: Number(pensionId),
    option_id: optionId.value,
  }
  store.joinProduct(payload)
}
</script>

<style scoped>

</style>