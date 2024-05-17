<template>
  <div>
    <form @submit.prevent="modifyUser">
        <label for="userId">아이디: </label>
        <input type="text" id="userId" :value="userInfo.userId" disabled>
        <br>
        <label for="nickname">닉네임: </label>
        <input type="text" id="nickname" placeholder="닉네임" v-model="userInfo.nickName">
        <br>
        <label for="userName">이름: </label>
        <input type="text" id="userName" :value="userInfo.userName" disabled>
        <br>
        <label for="gender">성별: </label>
        <select id="gender" v-model="userInfo.gender">
            <option value="남자">남자</option>
            <option value="여자">여자</option>
        </select>
        <br>
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
        <br>
        <label for="wealth">자산: </label>
        <input type="number" id="wealth" v-model="userInfo.wealth">
        <span>만원</span>
        <br>
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