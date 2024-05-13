<template>
  <div>
    <header>
      <nav class="bg-warning">
        <!-- 로고 글씨 대신 로고 이미지 삽입 예정 -->
        <router-link :to="{ name : 'home' }">로고</router-link>
        <router-link to="">예금</router-link>
        <router-link to="">적금</router-link>
        <router-link to="">연금</router-link>
        <router-link to="">대출</router-link>
        <router-link to="">근처 은행 찾기</router-link>
        <!-- 로그인 안했을 경우 -->
        <router-link :to="{ name : 'login' }">로그인</router-link>
        <router-link :to="{ name : 'signup' }">회원가입</router-link>
        <!-- 로그인 했을 경우 -->
        <router-link to="">로그아웃</router-link>
        <router-link :to="{ name : 'signup' }">회원가입</router-link>
      </nav>
    </header>
  </div>
</template>

<script setup>
</script>

<style scoped>
/* 임시 css -> 차후 부트스트랩으로 변경 및 수정 예정 */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}
</style>