<template>
  <div>
    <RouterLink to="/">로고</RouterLink>
    <h1>LOGIN</h1>
    <form @submit.prevent="logIn">
      <label for="userId">아이디: </label>
      <input type="text" id="userId" placeholder="아이디" v-model="userId">   
      <br>
      <label for="password">비밀번호: </label>
      <input type="password" id="password" placeholder="비밀번호" v-model="password">
      <br>
      <button type="submit">로그인</button>
    </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const userId = ref('')
const password = ref('')

const logIn = function() {
  const payload = {
    username: userId.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
</style>