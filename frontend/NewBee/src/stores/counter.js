import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useCounterStore = defineStore('counter', () => {
  const token = ref(null)
  const userInfo = ref(null)
  // 회원가입
  const signUp = function(info) {
    axios.post('http://127.0.0.1:8000/accounts/register/', info)
      .then(res => {
        console.log(res)
        console.log('회원가입이 완료되었습니다.')
        goLogin()
      })
      .catch(err => {
        console.log(err)
        // 에러 종류별 메시지 출력
        alert('회원가입에 실패하였습니다.')
      })
    }
  // 로그인
  const logIn = function(info) {
    axios.post('http://127.0.0.1:8000/accounts/auth/', info)
      .then(res => {
        console.log(res)
        console.log('로그인이 완료되었습니다.')
        // 유저 정보 및 토큰 저장 
        token.value = res.data.token
        userInfo.value = res.data
        // 로그인 완료 -> 메인 페이지로 이동
        goHome()
      })
      .catch(err => {
        console.log(err)
      })
    }
  // 메인 페이지로 이동
  const goHome = function() {
    router.push('/')
  }
  // 로그인 페이지로 이동
  const goLogin = function() {
    router.push('/login')
  }

  return { signUp, logIn, goHome, goLogin }
})
