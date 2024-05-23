<template>
  <div>
    <div class="card" style="width: 18rem;">
      <div class="card-header fw-bold fs-5">
        인기 대출 상품
      </div>
      <ul class="list-group list-group-flush">
        <li @click="goLoanDetail(best)" class="list-group-item item-hover" v-for="best in bestProduct.rent_loan"
          :key="best.id">{{ best.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const bestProduct = store.bestProduct

const goLoanDetail = (best) => {
  store.getLoanDetail(best.id).then(() => {
    router.push({ name: 'loanDetail', params: { id: best.id } })
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
