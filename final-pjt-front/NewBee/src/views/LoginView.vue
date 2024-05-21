<template>
  <div class="text-center">
    <Logo class="mb-3" />
    <h1 class="mb-4">로그인</h1>
    <div class="container">
      <form @submit.prevent="logIn">
        <div class="mb-3 form-floating">
          <input type="text" id="userId" class="form-control" placeholder="아이디" v-model="userId">   
          <label for="userId" class="form-label">아이디</label>
        </div>
        <div class="mb-4 form-floating">
          <input type="password" id="password" class="form-control" placeholder="비밀번호" v-model="password">
          <label for="password">비밀번호</label>
        </div>
        <button type="submit" class="btn btn-primary">로그인</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import Logo from '@/components/Logo.vue'

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