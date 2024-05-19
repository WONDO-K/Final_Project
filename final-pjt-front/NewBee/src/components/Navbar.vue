<template>
  <div class="mb-3">
    <header>
      <nav class="bg-warning rounded-3">
        <Logo />
        <router-link to="" class="h3 text-info text-decoration-none">예금</router-link>
        <router-link to="" class="h3 text-info text-decoration-none">적금</router-link>
        <router-link to="" class="h3 text-info text-decoration-none">연금</router-link>
        <router-link to="" class="h3 text-info text-decoration-none">대출</router-link>
        <router-link :to="{ name : 'banksearch'}" class="h3 text-info text-decoration-none">근처 은행 찾기</router-link>
        <router-link :to="{ name: 'freeboard' }" class="h3 text-info text-decoration-none">자유게시판</router-link>
        <!-- 로그인 안했을 경우 -->
        <router-link :to="{ name : 'login' }" v-show="!store.isLogin" class="h3 text-info text-decoration-none">로그인</router-link>
        <router-link :to="{ name : 'signup' }" v-show="!store.isLogin" class="h3 text-info text-decoration-none">회원가입</router-link>
        <!-- 로그인 했을 경우 -->
        <router-link :to="{ name : 'mypage' }" @click="getUser" v-show="store.isLogin" class="h3 text-info text-decoration-none">마이페이지</router-link>
        <a href="" class="h3 text-info text-decoration-none" @click="logOut" v-show="store.isLogin">로그아웃</a>
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