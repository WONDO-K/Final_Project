<template>
  <div class="container mt-4 text-center">
    <div class="card">
      <div class="card-body">
        <h1 class="card-title fw-bold">{{ loanDetail.fin_prdt_nm }}</h1>
        <p class="card-text"><strong>금융회사명:</strong> {{ loanDetail.kor_co_nm }}</p>
        <p class="card-text"><strong>대출 부대비용:</strong> {{ loanDetail.loan_inci_expn }}</p>
        <p class="card-text"><strong>조기 상환 수수료:</strong> {{ loanDetail.erly_rpay_fee }}</p>
        <p class="card-text"><strong>연체 이자율:</strong> {{ loanDetail.dly_rate }}</p>
        <p class="card-text"><strong>대출 한도:</strong> {{ loanDetail.loan_lmt }}</p>
        <p class="card-text"><strong>가입방법:</strong> {{ loanDetail.join_way }}</p>

        <h4 class="mt-4">상품 가입하기</h4>
        <div class="mb-3">
          <label for="optionSelect" class="form-label">옵션 선택</label>
          <select id="optionSelect" v-model="optionId" class="form-select">
            <option disabled value="">옵션을 선택해주세요</option>
            <option v-for="(option, index) in loanDetail.rent_loan_options" :value="index + 1" :key="index">
              상환 방식: {{ option.lend_rate_type_nm }},
              납부: {{ option.rpay_type_nm }},
              기본 금리: {{ option.lend_rate_avg }}%,
              최저 금리: {{ option.lend_rate_min }}%,
              최고 금리: {{ option.lend_rate_max }}%
            </option>
          </select>
        </div>
        <button class="btn btn-primary fw-bold" @click="joinLoan">가입</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const loanDetail = store.loanDetail
const loanId = route.params.id
const optionId = ref('')

const joinLoan = function () {
  const payload = {
    product_type: '전세대출',
    product_id: Number(loanId),
    option_id: optionId.value,
  }
  store.joinProduct(payload)
}

const getLoanDetail = function () {
  store.getLoanDetail(loanId)
}

getLoanDetail()
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.card-text {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.form-label {
  font-weight: bold;
}

.form-select {
  width: 100%;
}
</style>
