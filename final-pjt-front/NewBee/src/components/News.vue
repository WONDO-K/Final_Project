<template>
  <div>
    <div class="card text-center border-primary" style="width: 18rem;">
      <div class="card-header fw-bold fs-5">
        오늘의 뉴스
      </div>
      <div class="card-body">
        <p v-for="item in news" :key="item.originallink" >
          <a :href="item.originallink" target="_blank" style="color: black; text-decoration: none;">{{ cleanText(item.title) }}</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const news = ref([])
const getNews = function () {
  axios.get('http://127.0.0.1:8000/news/search/')
    .then(res => {
      console.log(res.data.results)
      console.log('뉴스를 가져왔습니다.')
      news.value = res.data.results
    })
    .catch(err => {
      console.log(err)
    })
}

const cleanText = (text) => {
  // HTML 태그 제거 및 한글만 추출하는 정규식
  return text.replace(/<\/?[^>]+(>|$)/g, '').replace(/[^ㄱ-ㅎㅏ-ㅣ가-힣\s]/g, '')
}

onMounted(() => {
  getNews()
})
</script>

<style scoped></style>
