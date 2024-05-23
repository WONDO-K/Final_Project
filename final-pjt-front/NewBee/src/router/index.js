import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
// 유저 관련
import MyPageView from '@/views/MyPageView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import PasswordChangeView from '@/views/PasswordChangeView.vue'
import MyProductView from '@/views/MyProductView.vue'
// 은행 관련
import BankSearchView from '@/views/BankSearchView.vue'
// 커뮤니티 관련
import FreeBoardView from '@/views/FreeBoardView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
// 상품 관련
import DepositsListView from '@/views/DepositsListView.vue'
import SavingsListView from '@/views/SavingsListView.vue'
import PensionListView from '@/views/PensionListView.vue'
import LoanListView from '@/views/LoanListView.vue'

// 상품 상세보기
import DepositDetailView from '@/views/DepositDetailView.vue'
import SavingDetailView from '@/views/SavingDetailView.vue'
import PensionDetailView from '@/views/PensionDetailView.vue'
import LoanDetailView from '@/views/LoanDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
    },
    {
      path: '/passwordchange',
      name: 'passwordChange',
      component: PasswordChangeView,
    },
    {
      path: '/banksearch',
      name: 'banksearch',
      component: BankSearchView,
    },
    {
      path: '/freeboard',
      name: 'freeboard',
      component: FreeBoardView,
    },
    {
      path: '/createarticle',
      name: 'createarticle',
      component: ArticleCreateView,
    },
    {
      path: '/article/:id',
      name: 'articleDetail',
      component: ArticleDetailView,
    },
    {
      path: '/article/:id/update',
      name: 'articleUpdate',
      component: ArticleUpdateView,
    },
    {
      path: '/depositslist',
      name: 'depositsList',
      component: DepositsListView,
    },
    {
      path: '/savingslist',
      name: 'savingsList',
      component: SavingsListView,
    },
    {
      path: '/pensionlist',
      name: 'pensionList',
      component: PensionListView,
    },
    {
      path: '/loanlist',
      name: 'loanList',
      component: LoanListView,
    },
    {
      path: '/depositdetail/:id/',
      name: 'depositDetail',
      component: DepositDetailView,
    },
    {
      path: '/savingdetail/:id/',
      name: 'savingDetail',
      component: SavingDetailView,
    },
    {
      path: '/pensiondetail/:id/',
      name: 'pensionDetail',
      component: PensionDetailView,
    },
    {
      path: '/loandetail/:id/',
      name: 'loanDetail',
      component: LoanDetailView,
    },
    {
      path: '/myproduct',
      name: 'myProduct',
      component: MyProductView
    },
  ]
})

export default router
