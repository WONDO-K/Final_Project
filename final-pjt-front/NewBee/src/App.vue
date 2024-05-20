<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const route = useRoute()
const store = useCounterStore()
const isRequest = store.isRequest
const changeRequest = store.changeRequest

// 은행 목록 API 요청 호출
const getBanks = async function () {
  try {
    const res = await axios.get('http://127.0.0.1:8000/products/banks/')
    console.log('은행 목록을 가져왔습니다.')
    console.log(res.data)
  } catch (err) {
    console.log(err)
  }
}

// 예금 목록 API 요청 호출
const getDeposits = async function () {
  try {
    const res = await axios.get('http://127.0.0.1:8000/products/deposit/register/')
    console.log('예금 상품 정보를 가져왔습니다.')
    console.log(res.data)
  } catch (err) {
    console.log(err)
  }
}

// 연금 목록 API 요청 호출
const getPensions = async function () {
  try {
    const res = await axios.get('http://127.0.0.1:8000/products/pension/register/')
    console.log('연금 상품 정보를 가져왔습니다.')
  } catch (err) {
    console.log(err)
  }
}

// 대출 목록 API 요청 호출
const getRentLoans = async function () {
  try {
    const res = await axios.get('http://127.0.0.1:8000/products/rent-loan/register/')
    console.log('대출 상품 정보를 가져왔습니다.')
  } catch (err) {
    console.log(err)
  }
}

// 적금 목록 API 요청 호출
const getSavings = async function () {
  try {
    const res = await axios.get('http://127.0.0.1:8000/products/saving/register/')
    console.log('적금 상품 정보를 가져왔습니다.')
  } catch (err) {
    console.log(err)
  }
}

onMounted(async () => {
  if (isRequest === false) {
    await getBanks()
    await getDeposits()
    await getPensions()
    await getRentLoans()
    await getSavings()
    changeRequest()
  }
})

</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- LoginView, SignupView Navbar 렌더링 X -->
    <Navbar v-if="route.name !== 'login' && route.name !== 'signup'" />
    <router-view />
    <Footer class="mt-auto"/>
  </div>

  
</template>

<style scoped>
</style>