<template>
  <div class="text-center">
    <Logo class="mb-3"/>
    <h1 class="mb-4">회원가입</h1>
    <div class="container">
      <form @submit.prevent="signUp">
        <div class="mb-3">
          <label for="userId" class="visually-hidden">아이디</label>
          <input type="text" id="userId" class="form-control text-center mb-2" placeholder="아이디" v-model="userId">
          <button type="button" class="btn btn-primary text-white" @click="checkId">중복 체크</button>
        </div>
        <div class="mb-3">
          <label for="password" class="visually-hidden">비밀번호</label>
          <input type="password" id="password" class="form-control text-center" placeholder="비밀번호" v-model="password">
        </div>
        <div class="mb-3">
          <label for="password" class="visually-hidden">비밀번호 확인</label>
          <input type="password" id="passwordCheck" class="form-control text-center" placeholder="비밀번호 확인" v-model="passwordCheck">
          <small v-show="!isPasswordMatch">비밀번호가 일치하지 않습니다.</small>
        </div>
        <div class="mb-3">
          <label for="userName" class="visually-hidden">이름</label>
          <input type="text" id="userName" class="form-control text-center" placeholder="이름" v-model="userName">
        </div>
        <div class="mb-3">
          <label for="nickname" class="visually-hidden">닉네임</label>
          <input type="text" id="nickname" class="form-control text-center" placeholder="닉네임" v-model="nickName">
        </div>
        <div class="mb-3">
          <label for="gender" class="visually-hidden">성별</label>
          <select id="gender" class="form-select" v-model="gender">
            <option disabled value="성별" class="text-center">성별</option>
            <option value="남자">남자</option>
            <option value="여자">여자</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="birth" class="form-label">생년월일</label>
          <input type="date" id="birth" class="form-control text-center" v-model="birth">
        </div>
        <div class="mb-3">
          <label for="email" class="visually-hidden">이메일</label>
          <input type="email" id="email" class="form-control text-center mb-2" placeholder="이메일" v-model="email">
          <button type="button" class="btn btn-primary text-white" @click="checkEmail">중복 체크</button>
        </div>
        <div class="mb-3">
          <label for="salary" class="form-label">연봉(단위: 만원)</label>
          <input type="number" id="salary" class="form-control text-center" v-model="salary">
        </div>
        <div class="mb-4">
          <label for="wealth">자산(단위:만원)</label>
          <input type="number" id="wealth" class="form-control text-center" v-model="wealth">
        </div>
        <button type="submit" class="btn btn-primary text-white" @click="signUp">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import Logo from '@/components/Logo.vue'

const store = useCounterStore()
const userId = ref('')
const password = ref('')
const passwordCheck = ref('')
const nickName = ref('')
const userName = ref('')
const gender = ref('성별')
const birth = ref('')
const email = ref('')
const salary = ref(0)
const wealth = ref(0)
const isPasswordMatch = computed(() => password.value === passwordCheck.value? true : false)

// 회원가입 버튼 클릭 시, 회원가입 함수 실행
const signUp = function() {
  const payload = {
      username: userId.value,
      password: password.value,
      password2: passwordCheck.value,
      nickname: nickName.value,
      realname: userName.value,
      email: email.value,
      birth: birth.value,
      salary: salary.value,
      gender: gender.value,
      wealth: wealth.value
  }
  store.signUp(payload)
}

// 아이디 중복 체크 함수
const checkId = function(){
  axios.get('http://127.0.0.1:8000/accounts/register/check-username/', {
    params: {
      username: userId.value
    }
  })
    .then((res) => {
      console.log(res)
      console.log('사용 가능한 아이디입니다.')
      alert('사용 가능한 아이디입니다.')
    })
    .catch((err) => {
      if (err.response.status === 500) {
        console.log('아이디 형식이 올바르지 않습니다.')
        alert('아이디 형식이 올바르지 않습니다.')
      } else {
        alert(err.response.data.message)
      }
    })
}

// 이메일 중복 체크 함수
const checkEmail = function(){
  axios.get('http://127.0.0.1:8000/accounts/register/check-email/', {
    params: {
      email: email.value
    }
  })
    .then((res) => {
      console.log(res)
      console.log('사용 가능한 이메일입니다.')
      alert('사용 가능한 이메일입니다.')
    })
    .catch((err) => {
      console.log(err)
      if (err.response.status === 500){
        console.log('이메일 형식이 올바르지 않습니다.')
        alert('이메일 형식이 올바르지 않습니다.')
      } else {
        alert(err.response.data.message)
      }
    })
}

</script>

<style scoped>
</style>