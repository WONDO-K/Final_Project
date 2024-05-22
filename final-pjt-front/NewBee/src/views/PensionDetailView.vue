<template>
  <div>
    <h1>금융상품명: {{ pensionDetail.fin_prdt_nm }}</h1>
    <p>금융회사명: {{ pensionDetail.kor_co_nm }}</p>
    <p>가입방법: {{ pensionDetail.join_way }}</p>
    <p>종류: {{ pensionDetail.pnsn_kind_nm }}</p>
    <p>유형: {{ pensionDetail.prdt_type_nm }}</p>
    <p>최저 보증이율: {{ pensionDetail.guar_rate }}%</p>
    <p>공시 이율: {{ pensionDetail.dcls_rate }}%</p>
    <p>전년도 수익율: {{ pensionDetail.btrm_prft_rate_1 }}%</p>
    <p>판매사: {{ pensionDetail.sale_co }}</p>
    
    <h2>상품 가입하기</h2>
    <div>
      <label>옵션 선택</label>
      <select v-model="optionId">
        <option disabled value="" class="text-center">옵션을 선택해주세요</option>
        <option v-for="(option, index) in pensionDetail.pension_options
          " :value="index + 1" :key="index">
          수령 기간: {{ option.pnsn_recp_trm_nm }} /
          가입 나이 : {{ option.pnsn_entr_age }}세 /
          월 납입액: {{ option.mon_paym_atm_nm }} /
          납입기간: {{ option.paym_prd_nm }} /
          연금 수령 나이: {{ option.pnsn_strt_age }}세 /
          연금 수령 금액: {{ option.pnsn_recp_amt }}원
        </option>
      </select>
    </div>
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
const optionId = ref('')
const pensionDetail = store.pensionDetail

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