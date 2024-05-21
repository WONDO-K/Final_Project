<template>
  <div class="container text-center">
    <h1>대출</h1>
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in loanList">
          <th scope="row">{{ loan.kor_co_nm }}</th>
          <td>{{ loan.fin_prdt_nm }}</td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const loanList = store.loanList

</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>