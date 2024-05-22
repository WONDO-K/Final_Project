<template>
  <div>
    <div class="text-center">
      <Logo class="mb-3" />
      <h1 class="mb-4">비밀번호 변경</h1>
      <div class="container">

        <form @submit.prevent="changePassword">
          <div class="mb-3 form-floating">
            <input type="password" id="now" class="form-control" placeholder="현재 비밀번호" v-model="now">   
            <label for="now" class="form-label">현재 비밀번호</label>
          </div>

          <div class="mb-3 form-floating">
              <input type="password" id="new1" class="form-control" placeholder="아이디" v-model="new1">   
              <label for="new1" class="form-label">새 비밀번호</label>
          </div>

          <div class="mb-4 form-floating">
            <input type="password" id="new2" class="form-control" placeholder="비밀번호" v-model="new2">
            <label for="new2">새 비밀번호 확인</label>
          </div>

          <button type="submit" class="btn btn-primary">변경</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const now = ref('')
const new1 = ref('')
const new2 = ref('')

const changePassword = function() {
  const payload = {
    old_password: now.value,
    new_password: new1.value,
    new_password2: new2.value
  }
  store.changePassword(payload)
}
</script>

<style scoped>
</style>