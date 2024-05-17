<template>
  <div class="container text-center">
    <form @submit.prevent="modifyUser">
      <div class="mb-3 form-floating">
        <input type="text" id="userId" class="form-control" :value="userInfo.userId" disabled>
        <label for="userId" class="form-label">아이디</label>
      </div>
      <div class="mb-3 form-floating">
        <input type="text" id="nickname" class="form-control" placeholder="닉네임" v-model="userInfo.nickName">
        <label for="nickname" class="form-label">닉네임</label>
      </div>
      <div class="mb-3 form-floating">
        <input type="text" id="userName" class="form-control" :value="userInfo.userName" disabled>
        <label for="userName" class="form-label">이름</label>
      </div>
      <div>
        <label for="gender" class="form-label visually-hidden">성별</label>
        <select id="gender" class="form-select" v-model="userInfo.gender">
            <option value="남자">남자</option>
            <option value="여자">여자</option>
        </select>
      </div>
      <label for="birth">생년월일: </label>
      <input type="text" id="birth" :value="userInfo.birth" disabled>
      <br>
      <label for="email">이메일: </label>
      <input type="email" id="email" :value="userInfo.email" disabled>
      <br>
      <!-- 단위: 만원 -->
      <label for="salary">연봉: </label>
      <input type="number" id="salary" v-model="userInfo.salary">
      <span>만원</span>
      <div>
        <label for="wealth">자산(단위: 만원)</label>
        <input type="number" id="wealth" v-model="userInfo.wealth">
      </div>
      <button type="submit" @click="modifyUser">수정</button>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const userInfo = store.userInfo

const modifyUser = function() {
  const payload = {
    nickname: userInfo.nickName,
    gender: userInfo.gender,
    salary: userInfo.salary,
    wealth: userInfo.wealth
  }
  store.modifyUser(payload)
}

</script>

<style scoped>
</style>