<template>
  <div>
    <div class="container text-center">
      <table class="table table-hover" v-if="savingsList && savingsList.length">
        <thead class="table-warning">
          <tr>
            <th scope="col">은행명</th>
            <th scope="col">상품명</th>
            <th scope="col">기본 금리</th>
            <th scope="col">최고 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="saving in displayedSavings" :key="saving.pk" @click="goSavingDetail(saving)">
            <th scope="row">{{ saving.kor_co_nm }}</th>
            <td>{{ saving.fin_prdt_nm }}</td>
            <td>{{ findMinAndMaxRate(saving.saving_options).minIntrRate }}%</td>
            <td>{{ findMinAndMaxRate(saving.saving_options).maxIntrRate2 }}%</td>
          </tr>
        </tbody>
      </table>
      <div v-else>
        데이터가 없습니다.
      </div>
      <button class="btn btn-primary" @click="prevPage"
        :disabled="currentPage === 0 || !savingsList || !savingsList.length">이전</button>
      <button class="btn btn-primary" @click="nextPage"
        :disabled="currentPage >= maxPage || !savingsList || !savingsList.length">다음</button>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

const store = useCounterStore()
const router = useRouter()
const savingsList = computed(() => store.savingsList || [])

const itemsPerPage = 10
const currentPage = ref(0)

const maxPage = computed(() => Math.ceil(savingsList.value.length / itemsPerPage) - 1)
const displayedSavings = computed(() => savingsList.value.slice(currentPage.value * itemsPerPage, (currentPage.value + 1) * itemsPerPage))

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

  if (minIntrRate === Infinity) {
    minIntrRate = '-';
  }
  if (maxIntrRate2 === -Infinity) {
    maxIntrRate2 = '-';
  }

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
