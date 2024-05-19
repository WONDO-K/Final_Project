<template>
  <div class="text-center">
    <h1 class="mb-4">자유게시판</h1>
    <div class="container mb-5">
      <ArticleList />
    </div>
    <router-link :to="{name: 'createarticle'}" v-show="isLogin"><button class="btn btn-primary text-white">글쓰기</button></router-link>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import ArticleList from '@/components/ArticleList.vue'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  store.getArticles()
})

const isLogin = store.isLogin



</script>

<style scoped>
</style>