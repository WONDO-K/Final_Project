import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import { Collapse } from 'bootstrap'

export const useCounterStore = defineStore('counter', () => {
  const token = ref(null)
  const userInfo = ref(null)
  const isLogin = computed(() => token.value !== null? true: false)
  
  // 메인 페이지로 이동
  const goHome = function() {
    router.push('/')
  }
  // 로그인 페이지로 이동
  const goLogin = function() {
    router.push('/login')
  }
  
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
    axios.delete('http://127.0.0.1:8000/accounts/auth/', info)
      .then(res => {
        console.log(res)
        console.log('로그인이 완료되었습니다.')
        // accessToken = res.data.token
        // refreshToken = res.data.refresh_token을 session storage에 저장
        // -> 유저 정보 요청할 때 보내야함

        // 유저 정보?? 저장 필요한가? 및 토큰 저장??
        // token.value = res.data.token
        // userInfo.value = res.data
        // 로그인 완료 -> 메인 페이지로 이동
        const cookies = document.cookie;
        const realToken = cookies.split('; ')[1]
        console.log(realToken)
        goHome()
      })
      .catch(err => {
        console.log(err)
       
      })
  }
  // 로그아웃 // 토큰 같은거 보내줘야하나?
  const logOut = function() {
    axios.delete('http://127.0.0.1:8000/accounts/auth/')
      .then(res => {
        console.log(res)
        console.log('로그아웃이 완료되었습니다.')
        // token.value = null
        // userInfo.value = null
        goHome()
      })
      .catch(err => {
        console.log(err)
      })
  }
  // 유저 정보 가져오기
  const getUser = function() {
    axios.get('http://127.0.0.1:8000/accounts/auth/')
      .then(res => {
        console.log(res)
        userInfo.value = res.data
      })
      .catch(err => {
        console.log(err)
      })
  }

  return { signUp, logIn, logOut, getUser, goHome, goLogin }
})