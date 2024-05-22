<template>
  <div>
    <div class="card text-center border-primary" style="width: 18rem;">
        <div class="card-header">
          오늘의 뉴스
        </div>
        <div class="card-body">
          <!-- <h5 class="card-title">소비자동향지수</h5> -->
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
          <p class="card-text">
            대충 뉴스 제목 링크들 어쩌구 저쩌구
          </p>
        </div>
        <button @click="getNews">안녕</button>
      </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

// const getNews = async () => {
//   try {
//     const response = await axios.get('https://openapi.naver.com/v1/search/news.json', {
//       headers: {
//         'X-Naver-Client-Id': 'NvN6J4EaKqHVd3h_lF2D',
//         'X-Naver-Client-Secret': 'rfuVjTp8eP'
//       },
//       params: {
//         query: 'hello',  // 검색어
//         display: 5,      // 검색 결과 출력 건수
//         start: 1         // 검색 시작 위치
//       }
//     });
//     console.log(response.data);
//   } catch (error) {
//     console.error('Error fetching news:', error.response ? error.response.data : error.message);
//   }
// }

onMounted(() => {
  // getNews()
})


</script>

<style scoped>

</style>