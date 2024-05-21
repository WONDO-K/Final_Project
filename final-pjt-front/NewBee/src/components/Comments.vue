<template>
  <div>
    <div v-for="comment in store.comments"
    :key="comment.id"
          :comment="comment" class="container">
      <td>[{{ comment.user }}] </td>
      <td>&nbsp;{{ comment.content }}</td>
      <td v-if="store.isLogin && (comment.user === store.userInfo.userId)">
        <button class="btn btn-primary" @click="toggleUpdateForm(comment.id)">수정</button>
      </td>
      <td v-if="store.isLogin && (comment.user === store.userInfo.userId)">
        <button class="btn btn-primary" @click="deleteComment(store.article.id, comment.id)">삭제</button>
      </td>
      <div v-if="isClicked[comment.id]">
        <td>
          <input type="text" :id="'update' + comment.id" v-model="updateContents[comment.id]" class="form-control">
        </td>
        <td>
          <button @click="updateComment(store.article.id, comment.id)" class="btn btn-primary">수정</button>
        </td>
      </div>
    </div>
    <div class="container mb-2">
      <input type="text" id="comment" class="form-control mb-3 mt-3" placeholder="댓글 쓰기(로그인하셔야 이용가능합니다.)" v-model="content">
      <button class="btn btn-primary" @click="createComment(store.article.id)" v-if="store.isLogin">댓글 등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()
const content = ref('')
const updateContents = reactive({}) // 각 댓글에 대한 수정 내용을 저장하는 객체
const isClicked = reactive({}) // 각 댓글에 대한 클릭 상태를 저장하는 객체

const toggleUpdateForm = function(commentId){
  if (isClicked[commentId]) {
    isClicked[commentId] = !isClicked[commentId]
  } else {
    isClicked[commentId] = true
  }
}

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
  isClicked[commentId] = false
}

const deleteComment = (articleId, commentId) => {
  store.deleteComment(articleId, commentId)
}

</script>

<style scoped>
</style>
