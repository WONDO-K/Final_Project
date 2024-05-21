<template>
  <div>
    <h1>{{ depositDetail.fin_prdt_nm }}</h1>

    <!-- 옵션 설렉트로 구성 -->
    <!-- 옵션 리스트의 index+1를 optionId로 사용 -->
    <select v-model="optionId">
      <option v-for="(option, index) in store.depositList[depositId].deposit_options" :key="index" :value="index+1">
        {{ option.option_nm }}
      </option>
    </select>

    <button class="btn btn-primary" @click="joinDeposit">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute() // 현재 라우트 정보를 가져옵니다.
const depositDetail = store.depositDetail

// deposit.pk 값은 route.params.id를 통해 접근할 수 있습니다.
const depositId = route.params.id
// null로 변경 후 v-model로 사용
const optionId = ref(1)

const joinDeposit = function(){
  const payload = {
    product_type: '정기예금',
    product_id: Number(depositId),
    option_id: optionId.value,
  }
  console.log(payload)
  store.joinProduct(payload)
}

</script>

<style scoped>
</style>