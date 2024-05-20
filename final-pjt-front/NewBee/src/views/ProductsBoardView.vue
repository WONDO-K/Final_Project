<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="!loading">
      <!-- 상태에 따라 렌더링 컴포넌트 변경-->

      <!-- 예금 상품 목록 표시 -->
      <DepositList />
      
      <!-- 적금 상품 목록 표시 -->
      <!-- <SavingsList /> -->

      <!-- 연금 상품 목록 표시 -->
      <!-- <PensionList /> -->

      <!-- 대출 상품 목록 표시 -->
      <!-- <LoanList /> -->
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import DepositList from '@/components/DepositList.vue'
import PensionList from '@/components/PensionList.vue'
import LoanList from '@/components/LoanList.vue'
import SavingsList from '@/components/SavingsList.vue'

const store = useCounterStore()
const loading = ref(true)
const isListRequest = store.isListRequest
const changeIsListRequest = store.changeIsListRequest

const requestList = async function(){
  if (isListRequest === false) {
    try {
      await store.getDepositList()
      await store.getPensionList()
      await store.getLoanList()
      await store.getSavingsList()
      changeIsListRequest()
    } catch (error) {
      console.error('Error fetching lists:', error)
    } finally {
      loading.value = false
    }
  } else {
    loading.value = false // 데이터가 이미 로드된 경우 로딩 상태만 false로 설정
  }
}

onMounted(() => {
  requestList()
})
</script>

<style scoped>
</style>