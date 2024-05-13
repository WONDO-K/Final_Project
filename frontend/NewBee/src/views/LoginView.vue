<template>
  <div>
    <h1>LOGIN</h1>
      <div class="login-box">
        <input type="text" placeholder="아이디" v-model="userId">
        <br>
        <input type="password" placeholder="비밀번호" v-model="userPassword">
        <br>
        <button type="submit" @click="loginSubmit">로그인</button>
      </div>
    </div>
</template>

<script setup>
// import { ref } from 'vue'
// userId = ref('')
// userPassword = ref('')

// const loginSubmit = function() {
//     axios.post('', {
//         id: userId.value, pw: userPassword.value
//     })
//     .then(response => {
//         console.log(response.data);
//     })
//     .catch(error => {
//         console.error(error);
//     })
// }
</script>

<style scoped>
</style>