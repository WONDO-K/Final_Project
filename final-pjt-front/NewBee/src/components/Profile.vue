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
      <div class="mb-3 form-floating">
        <select id="gender" class="form-select" v-model="userInfo.gender">
          <option value="남자">남자</option>
          <option value="여자">여자</option>
        </select>
        <label for="gender" class="form-label">성별</label>
      </div>
      <div class="mb-3 form-floating">
        <input type="text" id="birth" class="form-control" :value="userInfo.birth" disabled>
        <label for="birth" class="form-label">생년월일</label>
      </div>
      <div class="mb-3 form-floating">
        <input type="email" id="email" class="form-control" :value="userInfo.email" disabled>
        <label for="email" class="form-label">이메일</label>
      </div>
      <div class="mb-3 form-floating">
        <input type="number" id="salary" class="form-control" v-model="userInfo.salary">
        <label for="salary" class="form-label">연봉(단위: 만원)</label>
      </div>
      <div class="mb-4 form-floating">
        <input type="number" id="wealth" class="form-control" v-model="userInfo.wealth">
        <label for="wealth">자산(단위: 만원)</label>
      </div>
      <button type="submit" class="btn btn-primary text-white" @click="modifyUser">수정</button>
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