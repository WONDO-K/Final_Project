<template>
  <div class="container text-center">
    <h1>대출</h1>
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
          <th scope="col">평균 최저</th>
          <th scope="col">최저</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in loanList"
        key="loan.pk"
        @click="goLoanDetail(loan)">
          <th scope="row">{{ loan.kor_co_nm }}</th>
          <td>{{ loan.fin_prdt_nm }}</td>
          <td>{{ findMinAvgAndMinRate(loan.rent_loan_options).minAvgRate }}
            <span v-if="findMinAvgAndMinRate(loan.rent_loan_options).minAvgRate !== '-'">%</span>
          </td>
          <td>{{ findMinAvgAndMinRate(loan.rent_loan_options).minRate }}
            <span v-if="findMinAvgAndMinRate(loan.rent_loan_options).minAvgRate !== '-'">%</span>
          </td>
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
const loanList = store.loanList

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
  if (minAvgRate === Infinity){
    minAvgRate = '-'
  } else if (minRate === Infinity){
    minRate = '-'
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
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>
