<template>
  <div class="container mt-4 text-center">
    <div class="card">
      <div class="card-body">
        <h1 class="card-title fw-bold">{{ depositDetail.fin_prdt_nm }}</h1>
        <p class="card-text"><strong>금융회사명:</strong> {{ depositDetail.kor_co_nm }}</p>
        <p class="card-text"><strong>금융상품 설명:</strong> {{ depositDetail.etc_note }}</p>
        <p class="card-text"><strong>가입방법:</strong> {{ depositDetail.join_way }}</p>
        <p class="card-text"><strong>만기 후 이자율:</strong> {{ depositDetail.mtrt_int }}</p>
        <p class="card-text"><strong>우대조건:</strong> {{ depositDetail.spcl_cnd }}</p>

        <h4 class="mt-4">상품 가입하기</h4>
        <div class="mb-3">
          <label for="optionSelect" class="form-label">옵션 선택</label>
          <select id="optionSelect" v-model="optionId" class="form-select">
            <option disabled value="">옵션을 선택해주세요</option>
            <option v-for="(option, index) in depositDetail.deposit_options" :value="index + 1" :key="index">
              저축 유형: {{ option.intr_rate_type_nm }},
              저축 기간: {{ option.save_trm }}개월,
              기본 금리: {{ option.intr_rate }}%,
              우대 금리: {{ option.intr_rate2 }}%
            </option>
          </select>
        </div>
        <button class="btn btn-primary fw-bold" @click="joinDeposit">가입</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute() // 현재 라우트 정보를 가져옵니다.
const depositDetail = store.depositDetail

// deposit.pk 값은 route.params.id를 통해 접근할 수 있습니다.
const depositId = route.params.id
// null로 변경 후 v-model로 사용
const optionId = ref('')

const joinDeposit = function () {
  const payload = {
    product_type: '정기예금',
    product_id: Number(depositId),
    option_id: optionId.value,
  }
  console.log(payload)
  store.joinProduct(payload)
}

onMounted(() => {
  // store.getDepositsDetail()
})

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
