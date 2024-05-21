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
        <tr v-for="deposit in displayedDeposits"
        :key="deposit.pk"
        @click="goDepositDetail(deposit)">
          <th scope="row">{{ deposit.kor_co_nm }}</th>
          <td>{{ deposit.fin_prdt_nm }}</td>
          <td>{{ findMinAndMaxRate(deposit.deposit_options).minIntrRate }}%</td>
          <td>{{ findMinAndMaxRate(deposit.deposit_options).maxIntrRate2 }}%</td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-primary" @click="prevPage"  :disabled="currentPage === 0">이전</button>
    <button class="btn btn-primary" @click="nextPage" :disabled="currentPage >= maxPage">다음</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

const store = useCounterStore()
const router = useRouter()
const depositList = store.depositList

const itemsPerPage = 10
const currentPage = ref(0)

const maxPage = computed(() => Math.ceil(depositList.length / itemsPerPage) - 1)
const displayedDeposits = computed(() => depositList.slice(currentPage.value * itemsPerPage, (currentPage.value + 1) * itemsPerPage))

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
  store.getDepositDetail(deposit.pk).then(() => {
    router.push({ name: 'depositDetail', params: { id: deposit.pk } })
  })
}

const nextPage = () => {
  if (currentPage.value < maxPage.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 0) {
    currentPage.value--
  }
}
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>
