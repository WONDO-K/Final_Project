<template>
  <div>
    <div class="card" style="width: 18rem;">
      <div class="card-header fw-bold fs-5">
        추천 적금 상품
      </div>
      <ul class="list-group list-group-flush">
        <li @click="goSavingDetail(best)" class="list-group-item item-hover" v-for="best in recommendProduct.saving">{{ best.saving_product__fin_prdt_nm }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'


const store = useCounterStore()
const router = useRouter()
const recommendProduct = store.recommendProduct

const goSavingDetail = (best) => {
  store.getSavingDetail(best.saving_product).then(() => {
    router.push({ name: 'savingDetail', params: { id: best.saving_product } })
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