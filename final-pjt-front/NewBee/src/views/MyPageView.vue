<template>
  <div class="text-center">
    <h1 class="mb-4">마이페이지</h1>
    <router-link :to="{ name: 'myProduct'}">내가 가입한 상품 보기</router-link>
    <Profile />
    <router-link :to="{ name: 'passwordChange' }" class="btn btn-primary mt-3">비밀번호 변경</router-link>
    <button @click="singOut">회원탈퇴</button>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import Profile from '@/components/Profile.vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const singOut= function(){
  store.signOut()
}
</script>

<style scoped>
</style>