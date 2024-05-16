<template>
  <div>
    <header>
      <nav class="bg-warning">
        <Logo />
        <router-link to="">예금</router-link>
        <router-link to="">적금</router-link>
        <router-link to="">연금</router-link>
        <router-link to="">대출</router-link>
        <router-link :to="{ name : 'bank'}">근처 은행 찾기</router-link>
        <p>|</p>
        <!-- 로그인 안했을 경우 -->
        <router-link :to="{ name : 'login' }">로그인</router-link>
        <router-link :to="{ name : 'signup' }">회원가입</router-link>
        <!-- 로그인 했을 경우 -->
        <p>|</p>
        <router-link :to="{ name : 'mypage' }" @click="getUser">마이페이지</router-link>
        <button @click="store.logOut">로그아웃</button>
      </nav>
    </header>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter'
import Logo from './Logo.vue'

const store = useCounterStore()
const isLogin = store.isLogin
const getUser = store.getUser
</script>

<style scoped>
/* 임시 css -> 차후 부트스트랩으로 변경 및 수정 예정 */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>