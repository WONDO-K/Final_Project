<template>
    <div>
        <input type="text" placeholder="아이디" v-model="userId">
        <input type="password" placeholder="비밀번호" v-model="userPassword">
        <button type="submit" @click="loginSubmit">로그인</button>
    </div>
</template>

<script setup>
userId = ref('')
userPassword = ref('')

const loginSubmit = function() {
    axios.post('', {
        id: userId.value, pw: userPassword.value
    })
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
    })
}
</script>

<style scoped>
</style>