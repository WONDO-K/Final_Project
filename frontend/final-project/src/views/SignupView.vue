<template>
    <div>
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
            <option value="남자">남자</option>
            <option value="여자">여자</option>
        </select>
        <br>
        <label for="age">나이: </label>
        <input type="number" id="age" placeholder="나이" v-model="age">
        <br>
        <label for="birth">생년월일: </label>
        <input type="date" id="birth" placeholder="생년월일" v-model="birth">
        <br>
        <label for="phone">전화번호: </label>
        <input type="tel" id="phone" placeholder="전화번호" v-model="phoneNumber">
        <br>
        <label for="email">이메일: </label>
        <input type="email" id="email" placeholder="이메일" v-model="email">
        <br>
        <label for="salary">월급: </label>
        <input type="number" id="salary" placeholder="월급" v-model="salary">
        <br>
        <label for="wealth">자산: </label>
        <input type="number" id="wealth" placeholder="자산" v-model="wealth">
        <br>
        <label for="is_staff">관리자 여부: </label>
        <input type="checkbox" id="is_staff" v-model="isStaff">
        <br>
        <button type="submit" @click="signupSubmit">회원가입</button>
    </div>
</template>

<script setup>
const userInfo = {
    userId: ref(''),
    password: ref(''),
    passwordCheck: ref(''),
    nickname: ref(''),
    userName: ref(''),
    gender: ref(''),
    age: ref(0),
    birth: ref(''),
    phoneNumber: ref(''),
    email: ref(''),
    salary: ref(0),
    wealth: ref(0),
    isStaff: ref(false)
}

const checkId = function(){}
const checkNickname = function(){}
const signupSubmit = function(){}

</script>

<style scoped>

</style>