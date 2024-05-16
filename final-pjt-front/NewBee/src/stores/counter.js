import { ref, computed } from 'vue'
import { watch } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useCounterStore = defineStore('counter', () => {
  const userInfo = ref(null)

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
  // access 토큰 만료 시 refresh 토큰으로 재발급 logic 추가 필요
  const logIn = function(info) {
    axios.post('http://127.0.0.1:8000/accounts/auth/', info)
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        // 로컬 스토리지에 토큰 저장
        localStorage.setItem('access', res.data.token.access)
        localStorage.setItem('refresh', res.data.token.refresh)
        // 임시로 로그인 상태 변경
        isLogin.value = true
        // 로그인 완료 -> 메인 페이지로 이동
        goHome()
      })
      .catch(err => {
        console.log(err)
        alert('아이디 또는 비밀번호가 일치하지 않습니다.')
      })
  }
  // 로그아웃
  const logOut = function() {
    axios.delete('http://127.0.0.1:8000/accounts/auth/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`
      }
    })
      .then(res => {
        console.log('로그아웃이 완료되었습니다.')
        // 로컬 스토리지에서 토큰 삭제
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        goHome()
      })
      .catch(err => {
        console.log(err)
      })
  }
  // 유저 정보 가져오기
  const getUser = function() {
    axios.get('http://127.0.0.1:8000/accounts/auth/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`
      }})
      .then(res => {
        console.log(res)
        console.log('유저 정보를 가져왔습니다.')
      })
      .catch(err => {
        if (err.response) {
          // 서버로부터 응답을 받았지만 에러가 발생한 경우
          console.log(err.response.data);  // 에러 데이터
          console.log(err.response.status);  // 에러 코드
          console.log(err.response.headers);  // 응답 헤더
        } else if (err.request) {
          // 요청을 보내는 과정에서 에러가 발생한 경우
          console.log(err.request);  // 요청 정보
        } else {
          // 기타 에러
          console.log(err.message);
        }
        console.log(err.config);  // 요청 설정
      })
  }

  return {
    signUp, logIn, logOut, getUser,
    goHome, goLogin,
    isLogin
   }
})