<template>
  <div>
    <h1>금융상품명: {{ savingDetail.fin_prdt_nm }}</h1>
    <p>금융회사명: {{ savingDetail.kor_co_nm }}</p>
    <p>금융상품 설명: {{ savingDetail.etc_note }}</p>
    <p> 가입방법: {{ savingDetail.join_way }}</p>
    <p>만기 후 이자율: {{ savingDetail.mtrt_int }}</p>
    <p>우대조건: {{ savingDetail.spcl_cnd }}</p>

    <h2>상품 가입하기</h2>
      <div>
        <label>옵션 선택</label>
        <select v-model="optionId">
          <option disabled value="" class="text-center">옵션을 선택해주세요</option>
          <option v-for="(option, index) in savingDetail.saving_options
" :value="index + 1" :key="index">
            저축 유형: {{ option.intr_rate_type_nm }}
            저축 기간: {{ option.save_trm }}개월
            기본 금리: {{ option.intr_rate }}%
            우대 금리: {{ option.intr_rate2 }}%
          </option>
        </select>
      </div>
    <button class="btn btn-primary" @click="joinSaving">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'
import { onMounted } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()
const savingDetail = store.savingsDetail

const savingId = route.params.id
const optionId = ref('')

const joinSaving = function(){
  const payload = {
    product_type: '적금',
    product_id: Number(savingId),
    option_id: optionId.value,
  }
  store.joinProduct(payload)
}

onMounted(() => {
  store.getSavingDetail(savingId)
})

</script>

<style scoped>

</style>