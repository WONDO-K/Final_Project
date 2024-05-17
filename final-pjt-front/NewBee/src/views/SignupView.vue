<template>
  <div>
    <Logo />
    <h1>SIGNUP</h1>
    <form @submit.prevent="signUp">
      <!-- label에 작은 image 삽입 가능 혹은 label 삭제 가능 -->
      <!-- label 글자로 유지할 시, placeholder 삭제 -->        
      <label for="userId">아이디: </label>
      <input type="text" id="userId" placeholder="아이디" v-model="userId">
      <button type="button" @click="checkId">중복 체크</button>
      <br>
      <label for="password">비밀번호: </label>
      <input type="password" id="password" placeholder="비밀번호" v-model="password">
      <br>
      <label for="passwordCheck">비밀번호 확인: </label>
      <input type="password" id="passwordCheck" placeholder="비밀번호 확인" v-model="passwordCheck">
      <small v-show="!isPasswordMatch">비밀번호가 일치하지 않습니다.</small>
      <br>
      <label for="nickname">닉네임: </label>
      <input type="text" id="nickname" placeholder="닉네임" v-model="nickName">
      <br>
      <label for="userName">이름: </label>
      <input type="text" id="userName" placeholder="이름" v-model="userName">
      <br>
      <label for="gender">성별: </label>
      <select id="gender" v-model="gender">
          <option value="남자">남자</option>#$
          <option value="여자">여자</option>
      </select>
      <br>
      <label for="birth">생년월일: </label>
      <input type="date" id="birth" placeholder="생년월일" v-model="birth">
      <br>
      <label for="email">이메일: </label>
      <input type="email" id="email" placeholder="이메일" v-model="email">
      <button type="button" @click="checkEmail">중복 체크</button>
      <br>
      <!-- 단위: 만원 -->
      <label for="salary">연봉: </label>
      <input type="number" id="salary" placeholder="연봉" v-model="salary">
      <span>만원</span>
      <br>
      <label for="wealth">자산: </label>
      <input type="number" id="wealth" placeholder="자산" v-model="wealth">
      <span>만원</span>
      <br>
      <button type="submit" @click="signUp">회원가입</button>
    </form>
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
const gender = ref('')
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
/* 임시 css -> 차후 부트스트랩으로 변경 및 수정 예정 */
input {
    margin-bottom: 0.5rem;
    text-align: center
}
</style>