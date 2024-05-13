<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <div>
    <!-- LoginView, SignupView에선 Navbar, Footer 렌더링 안 할 예정  -->
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<style scoped>
</style>