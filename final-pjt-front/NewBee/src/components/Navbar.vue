<template>
  <div class="mb-3">
    <header>
      <nav class="bg-warning rounded-3">
        <Logo />
        <router-link to="">예금</router-link>
        <router-link to="">적금</router-link>
        <router-link to="">연금</router-link>
        <router-link to="">대출</router-link>
        <router-link :to="{ name : 'banksearch'}">근처 은행 찾기</router-link>
        <router-link :to="{ name: 'freeboard' }">자유게시판</router-link>
        <!-- 로그인 안했을 경우 -->
        <router-link :to="{ name : 'login' }" v-show="!store.isLogin">로그인</router-link>
        <router-link :to="{ name : 'signup' }" v-show="!store.isLogin">회원가입</router-link>
        <!-- 로그인 했을 경우 -->
        <router-link :to="{ name : 'mypage' }" @click="getUser" v-show="store.isLogin">마이페이지</router-link>
        <button class="btn btn-primary text-" @click="logOut" v-show="store.isLogin">로그아웃</button>
      </nav>
    </header>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter'
import Logo from './Logo.vue'

const store = useCounterStore()
const logOut = store.logOut
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