<template>
  <div class="container text-center">
    <h1>연금</h1>
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
          <th scope="col">연금 수령 정보</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pension in pensionList">
          <th scope="row">{{ pension.kor_co_nm }}</th>
          <td>{{ pension.fin_prdt_nm }}</td>
          <td>자세히 보기</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const pensionList = store.pensionList
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>