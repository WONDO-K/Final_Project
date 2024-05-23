<template>
  <div class="card" style="width: 18rem;">
    <div class="card-header fw-bold fs-5">
      추천 대출 상품
    </div>
    <ul class="list-group list-group-flush">
      <li @click="goLoanDetail(best)" class="list-group-item item-hover" v-for="best in recommendProduct.rent_loan">{{ best.rent_loan_product__fin_prdt_nm }}</li>
    </ul>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goLoanDetail = (best) => {
  store.getLoanDetail(best.pension_product).then(() => {
    router.push({ name: 'loanDetail', params: { id: best.rent_loan_product } })
  })
}
</script>

<style scoped>
.item-hover {
  cursor: pointer;
  transition: background-color 0.3s;
}

.item-hover:hover {
  background-color: #FFFFEF;
}
</style>