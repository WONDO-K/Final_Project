import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import { useRoute } from 'vue-router'


export const useCounterStore = defineStore('counter', () => {
  // 로그인 여부
  const isLogin = localStorage.getItem('access')? ref(true) : ref(false)
  
  const userInfo = ref({})
  const articles = ref([])
  const article = ref(null)
  const comments = ref(null)

  // 메인 페이지로 이동
  const goHome = function() {
    router.push('/')
  }
  // 로그인 페이지로 이동
  const goLogin = function() {
    router.push('/login')
  }

  // 회원가입
  const signUp = function(info){
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
        isLogin.value = true
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
        console.log(isLogin.value)
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        isLogin.value = false
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
        // 'Content-Type': 'application/json'
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
  // 게시글 목록 가져오기
  const getArticles = function() {
    axios.get('http://127.0.0.1:8000/articles/articles/')
      .then(res => {
        console.log('게시글을 가져왔습니다.')
        console.log(res.data)
        articles.value = res.data
      })
      .catch(err => {
        console.log(err)
      })
  }
  // 게시글 작성하기
  const createArticle = function(info) {
    axios.post('http://127.0.0.1:8000/articles/articles/', info, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('게시글이 작성되었습니다.')
        router.push('/freeboard')
      })
      .catch(err => {
        console.log(err)
      })    
  }
  // 게시글 상세정보 가져오기&댓글 가져오기
  const getArticle = function (id) {
    return axios.get(`http://127.0.0.1:8000/articles/articles/${id}/`)
      .then(res => {
        console.log('게시글 상세정보를 가져왔습니다.')
        console.log(res.data)
        article.value = res.data
        comments.value = res.data.comments
      })
      .catch(err => {
        console.log(err)
      })
  }

  // 게시글 삭제하기
  const deleteArticle = function(ArticleId) {
    axios.delete(`http://127.0.0.1:8000/articles/articles/${ArticleId}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('게시글이 삭제되었습니다.')
        router.push('/freeboard')
      })
      .catch(err => {
        console.log(err)
      })
  }

  // 게시글 수정하기
  const updateArticle = function (id, info) {
    axios.put(`http://127.0.0.1:8000/articles/articles/${id}/`, info, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('게시글이 수정되었습니다.')
        return getArticle(id)
      })
      .then(() => {
        router.push('/article/:id', { id: id })
      })
      .catch(err => {
        console.log(err)
      })
  }
  
  // 댓글 작성하기
  const createComment = function (articleId, content) {
    axios.post(`http://127.0.0.1:8000/articles/articles/${articleId}/comments/`, content, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
      .then(res => {
        console.log('댓글이 작성되었습니다.')
        return getArticle(articleId)
      })
      .then(() => {
        router.push('/article/:id', { id: articleId })
      })
      .catch(err => {
        console.log(err)
      })
  }
  // 댓글 수정하기
  const updateComment = function(articleId, commentId, content) {
    axios.put(`http://127.0.0.1:8000/articles/articles/${articleId}/comments/${commentId}/`, content, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
    .then(res => {
      console.log('댓글이 수정되었습니다.')
      getArticle(articleId)
      // router.push('/article/:id', { id: articleId })
    })
    .catch(err => {
      console.log(err)
    })
  }

  // 댓글 삭제하기 
  const deleteComment = function(articleId, commentId) {
    axios.delete(`http://127.0.0.1:8000/articles/articles/${articleId}/comments/${commentId}/`,{
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true // 쿠키를 요청에 포함시키는 옵션 추가
    })
    .then(res => {
      console.log('댓글이 삭제되었습니다.')
      getArticle(articleId)
      router.push('/article/:id', { id: articleId })
    })
    .catch(err => {
      console.log(err)
    })
  }

  return {
    goHome, goLogin,
    signUp, logIn, logOut, getUser, modifyUser,
    getArticles, createArticle, getArticle, deleteArticle, updateArticle,
    createComment, deleteComment, updateComment,
    isLogin, userInfo,
    articles, article,
    comments
   }
}, { persist: true })