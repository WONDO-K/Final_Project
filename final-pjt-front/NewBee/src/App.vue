<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- LoginView, SignupView Navbar 렌더링 X -->
    <Navbar v-if="route.name !== 'login' && route.name !== 'signup'" />
    <router-view />
    <Footer class="mt-auto"/>
  </div>
</template>

<style scoped>
</style>