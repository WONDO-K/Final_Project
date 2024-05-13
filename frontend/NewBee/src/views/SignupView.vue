<template>
    <div>
        <!-- 로고 글씨 대신 로고 이미지 삽입 예정 -->
      <RouterLink to="/">로고</RouterLink>
      <form @submit.prevent="signupSubmit">
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
        <br>
        <label for="nickname">닉네임: </label>
        <input type="text" id="nickname" placeholder="닉네임" v-model="nickname">
        <button type="button" @click="checkNickname">중복 체크</button>
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
        <!-- <label for="age">나이: </label>
        <input type="number" id="age" placeholder="나이" v-model="age">
        <br> -->
        <label for="birth">생년월일: </label>
        <input type="date" id="birth" placeholder="생년월일" v-model="birth">
        <br>
        <!-- <label for="phone">전화번호: </label>
        <input type="tel" id="phone" placeholder="전화번호" v-model="phoneNumber">
        <br> -->
        <label for="email">이메일: </label>
        <input type="email" id="email" placeholder="이메일" v-model="email">
        <br>
        <!-- 단위: 만원 -->
        <label for="salary">연봉: </label>
        <input type="number" id="salary" placeholder="연봉" v-model="salary">
        <span>만원</span>
        <br>
        <!-- 단위: 만원 -->
        <label for="wealth">자산: </label>
        <input type="number" id="wealth" placeholder="자산" v-model="wealth">
        <span>만원</span>
        <br>
        <!-- <label for="is_staff">관리자 여부: </label>
        <input type="checkbox" id="is_staff" v-model="isStaff">
        <br> -->
        <button type="submit">회원가입</button>
      </form>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue'

const userId = ref('')
const password = ref('')
const passwordCheck = ref('')
const nickname = ref('')
const userName = ref('')
const gender = ref('')
const birth = ref('')
const email = ref('')
const salary = ref(0)
const wealth = ref(0)

const checkId = function(){}
const checkNickname = function(){}

// 회원가입 정보를 서버로 전송
// 회원가입 성공 시, 로그인 페이지로 이동
// 회원가입 실패 시, 에러 메시지 출력
const signupSubmit = function(){
    const userInfo = {
        username: userId.value,
        password: password.value,
        password2: passwordCheck.value,
        nickname: nickname.value,
        realname: userName.value,
        nickname: nickname.value,
        email: email.value,
        birth: birth.value,
        salary: salary.value,
        gender: gender.value,
        wealth: wealth.value
    }
    // axios.post('http://localhost:8000/api/user/', userInfo)
    // .then(res => {
    //     console.log(res)
    //     // 로그인 페이지로 이동
    //     // this.$router.push('/login')
    // })
    // .catch(err => {
    //     console.log(err)
    //     // 에러 메시지 출력
    // })
}
</script>

<style scoped>
/* 임시 css -> 차후 부트스트랩으로 변경 및 수정 예정 */
input {
    margin-bottom: 0.5rem;
    text-align: center
}
</style>