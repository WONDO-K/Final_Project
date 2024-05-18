<template>
  <div class="text-center">
    <h1 class="mb-4">자유게시판</h1>
    <div class="container">
      <ArticleList />
    </div>
    <router-link :to="{name: 'createarticle'}">글쓰기</router-link>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import ArticleList from '@/components/ArticleList.vue'
import { RouterLink } from 'vue-router'

onMounted(() => {
  const store = useCounterStore()
  store.getArticles()
})

</script>

<style scoped>
</style>