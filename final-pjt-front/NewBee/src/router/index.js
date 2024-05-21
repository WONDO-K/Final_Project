import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import MyPageView from '@/views/MyPageView.vue'
import BankSearchView from '@/views/BankSearchView.vue'
// 커뮤니티 관련
import FreeBoardView from '@/views/FreeBoardView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
// 상품 관련
import ProductsBoardView from '@/views/ProductsBoardView.vue'
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
      path: '/productsboard',
      name: 'productsBoard',
      component: ProductsBoardView,
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
    }
  ]
})

export default router
