import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useCounterStore = defineStore('counter', () => {
  const userInfo = ref({})

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
    axios.post('http://127.0.0.1:8000/accounts/register/', info, {
      headers: {
        'Content-Type': 'application/json'
      }
      })
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
    axios.post('http://127.0.0.1:8000/accounts/auth/', info, {
      headers: {
        'Content-Type': 'application/json'
        }
      })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        // 로컬 스토리지에 토큰 저장
        localStorage.setItem('access', res.data.token.access)
        localStorage.setItem('refresh', res.data.token.refresh)
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
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
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
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('유저 정보를 가져왔습니다.')
        console.log(res.data)
        userInfo.value.userId = res.data.username
        userInfo.value.email = res.data.email
        userInfo.value.nickName = res.data.nickname
        userInfo.value.userName = res.data.realname
        userInfo.value.birth = res.data.birth
        userInfo.value.salary = res.data.salary
        userInfo.value.wealth = res.data.wealth
        userInfo.value.gender = res.data.gender
      })
      .catch(err => {
        console.log(err)
      })
    }
  // 유저 정보 수정
  const modifyUser = function(info) {
    axios.patch('http://127.0.0.1:8000/accounts/update/', info, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('유저 정보가 수정되었습니다.')
        goHome()
      })
      .catch(err => {
        console.log(err)
      })
  }

  return {
    signUp, logIn, logOut, getUser, modifyUser,
    goHome, goLogin,
    userInfo,
   }
})