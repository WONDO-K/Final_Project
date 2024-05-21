<template>
  <div>
    <h1>SavingDetailView</h1>
    <button @click="joinSaving">가입</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const savingId = route.params.id
const optionId = ref(1)

const joinSaving = function(){
  const payload = {
    product_type: '적금',
    product_id: Number(savingId),
    option_id: optionId.value,
  }
  store.joinProduct(payload)
}
</script>

<style scoped>

</style>