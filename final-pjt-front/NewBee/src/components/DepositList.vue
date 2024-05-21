<template>
  <div class="container text-center">
    <h1>예금</h1>
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="deposit in depositList">
          <th scope="row">{{ deposit.kor_co_nm }}</th>
          <td>{{ deposit.fin_prdt_nm }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="aaa">aaa</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const depositList = store.depositList

const aaa = () => {
  console.log(depositList[0])
  // store.changeIsListRequest()
}
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>