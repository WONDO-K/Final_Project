<template>
  <div>
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">번호</th>
          <th scope="col">제목</th>
          <th scope="col">내용</th>
          <th scope="col">댓글</th>
          <th scope="col">작성자</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in store.articles"
        :key="article.id"
        :article="article" @click="goDetail(article)">
          <th scope="row">{{ article.id }}</th>
          <td>{{ cutContent(article.title) }}</td>
          <td>{{ cutContent(article.content) }}</td>
          <td>{{ article.comments.length }}</td>
          <td>{{ article.user.username }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router';
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()

const cutContent = (content) => {
  return content.length > 10 ? content.slice(0, 10) + '...' : content;
}

const goDetail = (article) => {
  router.push({ name: 'articleDetail', params: { id: article.id }})
  store.getArticle(article.id)
}
</script>

<style scoped>
tr:hover {
  cursor: pointer;
}
</style>