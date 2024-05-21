<template>
  <div>
    <h1>대출 상세 정보</h1>
    <button @click="joinLoan">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute() // 현재 라우트 정보를 가져옵니다.

const loanId = route.params.id
const optionId = ref(1)

const joinLoan = function(){
  const payload = {
    product_type: '전세대출',
    product_id: Number(loanId),
    option_id: optionId.value,
  }
  console.log(payload)
  store.joinProduct(payload)
}
</script>

<style scoped>

</style>