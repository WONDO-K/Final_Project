<template>
  <div>
    <h1>My Page</h1>
    <!-- 수정할 수 있는 정보 / 수정할 수 있는 정보 구분해서 렌더링 차이 필요함 -->
    <button>수정</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const userInfo = ref(store.userInfo)
</script>

<style scoped>
</style>