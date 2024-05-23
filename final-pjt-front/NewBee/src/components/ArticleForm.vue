<template>
  <div>
    <div class="container">
      <form @submit.prevent="createArticle">
        <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input type="text" class="form-control" id="title" placeholder="제목을 입력하세요" v-model="title">
        </div>
        <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea class="form-control" id="content" rows="3" placeholder="내용을 입력하세요" v-model="content"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">작성</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const title = ref('')
const content = ref('')

const createArticle = function() {
  const payload = {
    title: title.value,
    content: content.value
  }
  store.createArticle(payload)
}

</script>

<style lang="scss" scoped>

</style>