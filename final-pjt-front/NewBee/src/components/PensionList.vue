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
        <tr v-for="pension in displayedPensions"
        :key="pension.pk"
        @click="goPensionDetail(pension)">
          <th scope="row">{{ pension.kor_co_nm }}</th>
          <td>{{ pension.fin_prdt_nm }}</td>
          <td>자세히 보기</td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-primary" @click="prevPage" :disabled="currentPage === 0">이전</button>
    <button class="btn btn-primary" @click="nextPage" :disabled="currentPage >= maxPage">다음</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

const store = useCounterStore()
const router = useRouter()
const pensionList = store.pensionList

const itemsPerPage = 10
const currentPage = ref(0)

const maxPage = computed(() => Math.ceil(pensionList.length / itemsPerPage) - 1)
const displayedPensions = computed(() => pensionList.slice(currentPage.value * itemsPerPage, (currentPage.value + 1) * itemsPerPage))

const goPensionDetail = (pension) => {
  store.getPensionDetail(pension.pk).then(() => {
    router.push({ name: 'pensionDetail', params: { id: pension.pk }})
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
