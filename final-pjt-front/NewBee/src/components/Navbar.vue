<template>
  <div class="mb-3">
    <header class="d-flex justify-content-between align-items-center py-3 me-3">
      <div class="d-flex align-items-center">
        <Logo />
        <!-- 로그인 회원가입 버튼 -->
        <div class="d-flex gap-2 ms-3">
          <!-- 로그인 안했을 경우 -->
          <router-link :to="{ name: 'login' }" v-show="!store.isLogin" class="btn btn-primary font-bold">
            로그인
          </router-link>
          <router-link :to="{ name: 'signup' }" v-show="!store.isLogin" class="btn btn-primary font-bold">
            회원가입
          </router-link>
          <!-- 로그인 했을 경우 -->
          <router-link :to="{ name: 'mypage' }" @click="getUser" v-show="store.isLogin" class="btn btn-primary font-bold">
            {{ store.userInfo.nickName }}님
          </router-link>
          <a class="btn btn-primary font-bold" @click="logOut" v-show="store.isLogin">로그아웃</a>
        </div>
      </div>
      <nav class="d-flex gap-3">
        <div class="dropdown">
          <button class="btn btn-primary dropdown-toggle font-bold" type="button" id="dropdownMenuButton"
            data-bs-toggle="dropdown" aria-expanded="false">
            상품 조회
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <li>
              <router-link :to="{ name: 'depositsList' }" class="dropdown-item font-bold">예금</router-link>
            </li>
            <li>
              <router-link :to="{ name: 'savingsList' }" class="dropdown-item font-bold">적금</router-link>
            </li>
            <li>
              <router-link :to="{ name: 'pensionList' }" class="dropdown-item font-bold">연금</router-link>
            </li>
            <li>
              <router-link :to="{ name: 'loanList' }" class="dropdown-item font-bold">대출</router-link>
            </li>
          </ul>
        </div>
        <router-link class="btn btn-primary font-bold" :to="{ name: 'banksearch' }">
          근처 은행 찾기
        </router-link>
        <router-link class="btn btn-primary font-bold" :to="{ name: 'freeboard' }">
          자유게시판
        </router-link>
      </nav>
    </header>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import Logo from './Logo.vue';

const store = useCounterStore();
const logOut = store.logOut;
const getUser = store.getUser;
</script>

<style scoped>
a:hover {
  cursor: pointer;
}

.font-bold {
  font-weight: bold;
}
</style>
