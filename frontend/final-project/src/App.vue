<script setup>

</script>

<template>
  <div>
    <header>
      <nav class="bg-warning">
          <!-- a 태그로 변경 가능 -->
          <router-link to=""><img src="" alt="">로고</router-link>
          <router-link to="">예금</router-link>
          <router-link to="">적금</router-link>
          <router-link to="">연금</router-link>
          <router-link to="">대출</router-link>
          <router-link to="">근처 은행 찾기</router-link>
          <!-- 로그인 안했을 경우 -->
          <router-link to="">로그인</router-link>
          <router-link to="">회원가입</router-link>
          <!-- 로그인 했을 경우 -->
          <router-link to="">로그아웃</router-link>
      </nav>
    </header>
    <router-view />
    <footer class="bg-primary">
      <p>© 2021. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

footer {
  text-align: center;
  padding: 1rem;
}
</style>