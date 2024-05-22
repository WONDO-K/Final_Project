<template>
  <div>
    <h1>대출 상세 정보</h1>
      <h1>금융상품명: {{ loanDetail.fin_prdt_nm }}</h1>
      <p>금융회사명: {{ loanDetail.kor_co_nm }}</p>
      <p>대출 부대비용: {{ loanDetail.loan_inci_expn }}</p>
      <p>조기 상환 수수료: {{ loanDetail.erly_rpay_fee }}</p>
      <p>연체 이자율: {{ loanDetail.dly_rate }}</p>
      <p>대출 한도: {{ loanDetail.loan_lmt }}</p>
      <p> 가입방법: {{ loanDetail.join_way }}</p>

    <h2>상품 가입하기</h2>
    <div>
      <label>옵션 선택</label>
      <select v-model="optionId">
        <option disabled value="" class="text-center">옵션을 선택해주세요</option>
        <option v-for="(option, index) in loanDetail.rent_loan_options
  " :value="index + 1" :key="index">
          상환 방식: {{ option.lend_rate_type_nm }}
          납부: {{ option.rpay_type_nm }}
          기본 금리: {{ option.lend_rate_avg
             }}%
          최저 금리: {{ option.lend_rate_min }}%
          최고 금리: {{ option.lend_rate_max }}%
        </option>
      </select>
    </div>
    <button class="btn btn-primary" @click="joinLoan">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute() // 현재 라우트 정보를 가져옵니다.

const loanDetail = store.loanDetail
const loanId = route.params.id
const optionId = ref('')

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