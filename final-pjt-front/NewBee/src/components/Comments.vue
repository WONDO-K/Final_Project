<template>
  <div>
    <h1>Comments</h1>
    <label for="comment">댓글</label>
    <input type="text" id="comment" v-model="content">
    <button @click="createComment(store.article.id)">등록</button>
    <div v-for="comment in store.comments"
         :key="comment.id">
      <p>{{ comment.content }}</p>
      <p>{{ comment.user }}</p>
      
      <div v-if="comment.user === store.userInfo.userId">
        <label for="update">댓글 수정</label>
        <input type="text" :id="'update' + comment.id" v-model="updateContents[comment.id]">
        <button @click="updateComment(store.article.id, comment.id)">진짜 수정</button>
        <br>
        <button>댓글 수정</button>
        <button @click="deleteComment(store.article.id, comment.id)">댓글 삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
const content = ref('')
const updateContents = reactive({}) // 각 댓글에 대한 수정 내용을 저장하는 객체

const createComment = function(articleId){
  const payload = {
    content: content.value
  }
  content.value = ''
  store.createComment(articleId, payload)
}

const updateComment = (articleId, commentId) => {
  const payload = {
    content: updateContents[commentId]
  }
  store.updateComment(articleId, commentId, payload)
  // 업데이트 후 입력 필드 초기화
  updateContents[commentId] = ''
}

const deleteComment = (articleId, commentId) => {
  store.deleteComment(articleId, commentId)
}

</script>

<style scoped>
</style>
