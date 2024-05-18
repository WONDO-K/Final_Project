<template>
  <div class="text-center">
    <h1 class="mb-4">게시글 상세 페이지</h1>
    <div class="container">
      <div class="mb-3">
        <label for="title" class="form-label">글 번호</label>
        <input type="text" class="form-control" id="title" :value="article.id" disabled>
      </div>
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input type="text" class="form-control" id="title" :value="article.title" disabled>
      </div>
      <div class="mb-3">
        <label for="writer" class="form-label">작성자</label>
        <input type="text" id="writer" class="form-control" :value="article.user.username" disabled>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea class="form-control" id="content" rows="3" :value="article.content" disabled></textarea>
      </div>
    </div>
    <!-- 댓글 목록 들어갈 예정 -->
    <!-- 글 작성자와 로그인한 유저가 같은지 확인 후 렌더링 -->
    <router-link :to="{ name: 'articleUpdate', params: { id: article.id } }" v-if="checkUser">
      <button type="submit" class="btn btn-primary text-white">수정</button>
    </router-link>
    <button type="submit" class="btn btn-primary text-white" @click="deleteArticle" v-if="checkUser">삭제</button>
  </div>
</template>

<script setup>
import router from '@/router';
import { useCounterStore } from '@/stores/counter'
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const store = useCounterStore()
const article = store.article
const isLogin = store.isLogin
const userInfo = store.userInfo
// 글 작성자와 로그인한 유저가 같은지 확인
const checkUser = computed(() => (isLogin && userInfo.userId === article.user.username)? true : false)

const deleteArticle = function(){
  store.deleteArticle(article.id)
}
</script>

<style scoped>
</style>