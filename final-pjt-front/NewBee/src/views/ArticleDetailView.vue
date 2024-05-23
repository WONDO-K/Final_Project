<template>
  <div class="text-center">
    <h1 class="mb-5">{{ article.title }}</h1>
    <div class="container mb-3">
      <div class="mb-3">
        <label for="title" class="form-label">번호</label>
        <input type="text" class="form-control" id="title" :value="article.id" disabled>
      </div>
      <div class="mb-3">
        <label for="writer" class="form-label">작성자</label>
        <input type="text" id="writer" class="form-control" :value="article.user" disabled>
      </div>
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input type="text" class="form-control" id="title" :value="article.title" disabled>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea class="form-control" id="content" rows="3" :value="article.content" disabled></textarea>
      </div>
      <p class="fw-bold">{{ store.articleLike }}명이 좋아요를 눌렀어요!</p>
      <button class="btn btn-primary fw-bold" @click="likeArticle">좋아요</button>
    </div>
    <!-- 글 작성자와 로그인한 유저가 같은지 확인 후 렌더링 -->
    <router-link :to="{ name: 'articleUpdate', params: { id: article.id } }" v-if="checkUser">
      <button type="submit" class="btn btn-primary mb-1 fw-bold">게시글 수정</button>
      <br>
    </router-link>
    <button type="submit" class="btn btn-primary mb-5 fw-bold" @click="deleteArticle" v-if="checkUser">게시글 삭제</button>
    <Comments />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import { useCounterStore } from '@/stores/counter'
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { onMounted } from 'vue';
import { useRoute } from 'vue-router'
import Comments from '@/components/Comments.vue'

const store = useCounterStore()
const route = useRoute()
const article = store.article
const isLogin = store.isLogin
const userInfo = store.userInfo
// 글 작성자와 로그인한 유저가 같은지 확인
const checkUser = computed(() => (isLogin && userInfo.userId === article.user)? true : false)

onMounted(() => {
  store.getArticle(article.id)
  store.getLike(article.id)
})

const likeArticle = function(){
  store.likeArticle(article.id)
}

const deleteArticle = function(){
  store.deleteArticle(article.id)
}

</script>

<style scoped>
</style>