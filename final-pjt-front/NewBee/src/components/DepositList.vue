<template>
  <div class="container text-center">
    <h1>예금</h1>
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
        <tr v-for="deposit in depositList"
        :key="deposit.id"
        @click="goDepositDetail(deposit)">
          <th scope="row">{{ deposit.kor_co_nm }}</th>
          <td>{{ deposit.fin_prdt_nm }}</td>
          <td>{{ findMinAndMaxRate(deposit.deposit_options).minIntrRate }}%</td>
          <td>{{ findMinAndMaxRate(deposit.deposit_options).maxIntrRate2 }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const depositList = store.depositList

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
  });

  return {
    minIntrRate,
    maxIntrRate2
  };
}

const goDepositDetail = (deposit) => {
  store.getArticle(deposit.id).then(() => {
    router.push({ name: 'depositDetail', params: { id: deposit.id } })
  })
}
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>
