<template>
  <div class="container text-center">
    <h1>대출</h1>
    <table class="table table-hover" v-if="loanList && loanList.length">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
          <th scope="col">평균 최저</th>
          <th scope="col">최저</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in displayedLoans" :key="loan.pk" @click="goLoanDetail(loan)">
          <th scope="row">{{ loan.kor_co_nm }}</th>
          <td>{{ loan.fin_prdt_nm }}</td>
          <td>{{ findMinAvgAndMinRate(loan.rent_loan_options).minAvgRate }}
            <span v-if="findMinAvgAndMinRate(loan.rent_loan_options).minAvgRate !== '-'">%</span>
          </td>
          <td>{{ findMinAvgAndMinRate(loan.rent_loan_options).minRate }}
            <span v-if="findMinAvgAndMinRate(loan.rent_loan_options).minRate !== '-'">%</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      데이터가 없습니다.
    </div>
    <button class="btn btn-primary" @click="prevPage"
      :disabled="currentPage === 0 || !loanList || !loanList.length">이전</button>
    <button class="btn btn-primary" @click="nextPage"
      :disabled="currentPage >= maxPage || !loanList || !loanList.length">다음</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

const store = useCounterStore()
const router = useRouter()
const loanList = computed(() => store.loanList || [])

const itemsPerPage = 10
const currentPage = ref(0)

const maxPage = computed(() => Math.ceil(loanList.value.length / itemsPerPage) - 1)
const displayedLoans = computed(() => loanList.value.slice(currentPage.value * itemsPerPage, (currentPage.value + 1) * itemsPerPage))

function findMinAvgAndMinRate(options) {
  let minAvgRate = Infinity;
  let minRate = Infinity;

  options.forEach(option => {
    const avgRate = parseFloat(option.lend_rate_avg);
    const rate = parseFloat(option.lend_rate_min);

    if (avgRate < minAvgRate) {
      minAvgRate = avgRate;
    }

    if (rate < minRate) {
      minRate = rate;
    }
  });

  if (minAvgRate === Infinity) {
    minAvgRate = '-';
  }
  if (minRate === Infinity) {
    minRate = '-';
  }

  return {
    minAvgRate,
    minRate
  };
}

const goLoanDetail = (loan) => {
  store.getLoanDetail(loan.pk).then(() => {
    router.push({ name: 'loanDetail', params: { id: loan.pk } })
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
