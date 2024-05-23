<template>
  <div class="container mt-4 text-center">
    <div class="card">
      <div class="card-body">
        <h1 class="card-title fw-bold">{{ pensionDetail.fin_prdt_nm }}</h1>
        <p class="card-text"><strong>금융회사명:</strong> {{ pensionDetail.kor_co_nm }}</p>
        <p class="card-text"><strong>종류:</strong> {{ pensionDetail.pnsn_kind_nm }}</p>
        <p class="card-text"><strong>가입방법:</strong> {{ pensionDetail.join_way }}</p>
        <p class="card-text"><strong>유형:</strong> {{ pensionDetail.prdt_type_nm }} {{ pensionDetail.mtrt_int }}</p>
        <p class="card-text"><strong>판매점:</strong> {{ pensionDetail.sale_co }} {{ pensionDetail.spcl_cnd }}</p>

        <h4 class="mt-4">상품 가입하기</h4>
        <div class="mb-3">
          <label for="optionSelect" class="form-label">옵션 선택</label>
          <select id="optionSelect" v-model="optionId" class="form-select">
            <option disabled value="">옵션을 선택해주세요</option>
            <option v-for="(option, index) in pensionDetail.pension_options" :value="index + 1" :key="index">
              매달 납입 금액: {{ option.mon_paym_atm_nm }},
              납입 기간: {{ option.paym_prd_nm}},
              납입 시작 나이: {{ option.pnsn_entr_age_nm
                 }}
              연금 수령 나이: {{ option.pnsn_strt_age_nm }},
            </option>
          </select>
        </div>
        <button class="btn btn-primary fw-bold" @click="joinPension">가입</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()
const pensionDetail = store.pensionDetail

const pensionId = route.params.id
const optionId = ref('')

const joinPension = function () {
  const payload = {
    product_type: '연금',
    product_id: Number(pensionId),
    option_id: optionId.value,
  }
  store.joinProduct(payload)
}

onMounted(() => {
  store.getPensionDetail(pensionId)
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
