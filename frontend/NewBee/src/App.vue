<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div>
    <!-- LoginView, SignupView에선 Navbar, Footer 렌더링 X -->
    <Navbar v-if="route.name !== 'login' && route.name !== 'signup'" />
    <router-view />
    <Footer v-if="route.name !== 'login' && route.name !== 'signup'" />
  </div>
</template>

<style scoped>
</style>