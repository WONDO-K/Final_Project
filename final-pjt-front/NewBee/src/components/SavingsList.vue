<template>
  <div class="container text-center">
    <table class="table table-hover">
      <thead class="table-warning">
        <tr>
          <th scope="col">은행명</th>
          <th scope="col">상품명</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="saving in savingsList">
          <th scope="row">{{ saving.kor_co_nm }}</th>
          <td>{{ saving.fin_prdt_nm }}</td>
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
const savingsList = store.savingsList
</script>

<style scoped>
</style>