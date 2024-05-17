<template>
  <div>
    <h1 class="text-center">자유게시판</h1>
    <div class="container">
      <ArticleList />
    </div>
    <router-link :to="{name: 'createarticle'}">글쓰기</router-link>
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { RouterLink } from 'vue-router'

</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
  border: 1px solid #ccc;
}
</style>