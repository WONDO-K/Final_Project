import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
  const token = ref(null)
  
  const signUp = function(info) {
    axios.post('http://127.0.0.1:8000/accounts/register/', info)
      .then(res => {
        console.log(res)
        console.log('회원가입이 완료되었습니다.')
        // 회원가입 완료 -> 로그인 페이지로 이동
      })
      .catch(err => {
        console.log(err)
        // 에러 메시지 출력
      })
    }

  const logIn = function(info) {
    axios.post('http://127.0.0.1:8000/accounts/auth/', info)
      .then(res => {
        console.log(res)
        console.log('로그인이 완료되었습니다.')
        // 토큰 저장
        token.value = res.data.token
        // 로그인 완료 -> 메인 페이지로 이동
      })
      .catch(err => {
        console.log(err)
        // 에러 메시지 출력
      })
    }

  return { signUp, logIn }
})
