<template>
  <div class="container text-center">
    <h1>적금</h1>
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
          <th scope="col">기본 금리</th>
          <th scope="col">최고 금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="saving in savingsList"
        :key="saving.pk"
        @click="goSavingDetail(saving)">
          <th scope="row">{{ saving.kor_co_nm }}</th>
          <td>{{ saving.fin_prdt_nm }}</td>
          <td>{{ findMinAndMaxRate(saving.saving_options).minIntrRate }}%</td>
          <td>{{ findMinAndMaxRate(saving.saving_options).maxIntrRate2 }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const savingsList = store.savingsList

function findMinAndMaxRate(options) {
  let minIntrRate = Infinity;
  let maxIntrRate2 = -Infinity;

  options.forEach(option => {
    const intrRate = parseFloat(option.intr_rate);
    const intrRate2 = parseFloat(option.intr_rate2);

    if (intrRate < minIntrRate) {
      minIntrRate = intrRate;
    }

    if (intrRate2 > maxIntrRate2) {
      maxIntrRate2 = intrRate2;
    }
  })

  return {
    minIntrRate,
    maxIntrRate2
  }
}

const goSavingDetail = (saving) => {
  store.getSavingDetail(saving.pk).then(() => {
    router.push({ name: 'savingDetail', params: { id: saving.pk } })
  })
}
</script>

<style scoped>
</style>