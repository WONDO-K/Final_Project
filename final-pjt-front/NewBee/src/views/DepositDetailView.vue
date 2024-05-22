<template>
  <div>
    <h1>금융상품명: {{ depositDetail.fin_prdt_nm }}</h1>
    <p>금융회사명: {{ depositDetail.kor_co_nm }}</p>
    <p>금융상품 설명: {{ depositDetail.etc_note }}</p>
    <p> 가입방법: {{ depositDetail.join_way }}</p>
    <p>만기 후 이자율: {{ depositDetail.mtrt_int }}</p>
    <p>우대조건: {{ depositDetail.spcl_cnd }}</p>
    
    <h2>상품 가입하기</h2>
    <div>
      <label>옵션 선택</label>
      <select v-model="optionId">
        <option disabled value="" class="text-center">옵션을 선택해주세요</option>
        <option v-for="(option, index) in depositDetail.deposit_options" :value="index + 1" :key="index">
          저축 유형: {{ option.intr_rate_type_nm }}
          <br>
          저축 기간: {{ option.save_trm }}개월
          <br>
          기본 금리: {{ option.intr_rate }}%
          우대 금리: {{ option.intr_rate2 }}%
        </option>
      </select>
    </div>
    <button class="btn btn-primary" @click="joinDeposit">가입</button>
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
  store.getDepositsDetail(depositId)
})

</script>

<style scoped>
</style>
