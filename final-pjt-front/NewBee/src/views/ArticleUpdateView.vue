<template>
  <div class="text-center">
    <h1 class="mb-4">게시글 수정 페이지</h1>
    <div class="container">
      <form @submit.prevent="updateArticle">
        <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input type="text" class="form-control" id="title" v-model="title">
        </div>
        <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea class="form-control" id="content" rows="3" v-model="content"></textarea>
        </div>
        <button type="submit" class="btn btn-primary text-white">수정</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
const store = useCounterStore()

const title = ref(store.article.title)
const content = ref(store.article.content)

const updateArticle = function() {
  const payload = {
    title: title.value,
    content: content.value
  }
  store.updateArticle(store.article.id, payload)
}
</script>

<style scoped>
</style>