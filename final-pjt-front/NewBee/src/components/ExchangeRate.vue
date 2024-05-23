<template>
  <div>
    <div class="card text-center border-primary" style="width: 40rem;">
      <div class="card-header fw-bold fs-5">
        오늘의 환율은?
      </div>
      <div class="card-body mb-3">
        <h5 class="card-title mb-4 fw-bold">환율계산기</h5>
        <label for="from" class="form-label fw-bold">FROM</label>
        <select id="from" class="form-control text-center mb-3" v-model="from">
          <option value="AED">AED(아랍에미리트 디르함)</option>
          <option value="AUD">AUD(호주 달러)</option>
          <option value="BHD">BHD(바레인 디나르)</option>
          <option value="BND">BND(브루나이 달러)</option>
          <option value="CAD">CAD(캐나다 달러)</option>
          <option value="CHF">CHF(스위스 프랑)</option>
          <option value="CNH">CNH(위안화)</option>
          <option value="DKK">DKK(덴마아크 크로네)</option>
          <option value="EUR">EUR(유로)</option>
          <option value="GBP">GBP(영국 파운드)</option>
          <option value="HKD">HKD(홍콩 달러)</option>
          <option value="IDR(100)">IDR(100)(인도네시아 루피아)</option>
          <option value="JPY(100)">JPY(100)(일본 옌)</option>
          <option value="KRW">KRW(한국 원)</option>
          <option value="KWD">KWD(쿠웨이트 디나르)</option>
          <option value="MYR">MYR(말레이지아 링기트)</option>
          <option value="NOK">NOK(노르웨이 크로네)</option>
          <option value="NZD">NZD(뉴질랜드 달러)</option>
          <option value="SAR">SAR(사우디 리얄)</option>
          <option value="SEK">SEK(스웨덴 크로나)</option>
          <option value="SGD">SGD(싱가포르 달러)</option>
          <option value="THB">THB(태국 바트)</option>
          <option value="USD">USD(미국 달러)</option>
        </select>
        <button class="btn btn-primary mb-3 fw-bold" @click="changeValue">↑↓</button>
        <br>
        <label for="TO" class="form-label fw-bold">TO</label>
        <select id="TO" class="form-control text-center" v-model="to">
          <option value="AED">AED(아랍에미리트 디르함)</option>
          <option value="AUD">AUD(호주 달러)</option>
          <option value="BHD">BHD(바레인 디나르)</option>
          <option value="BND">BND(브루나이 달러)</option>
          <option value="CAD">CAD(캐나다 달러)</option>
          <option value="CHF">CHF(스위스 프랑)</option>
          <option value="CNH">CNH(위안화)</option>
          <option value="DKK">DKK(덴마아크 크로네)</option>
          <option value="EUR">EUR(유로)</option>
          <option value="GBP">GBP(영국 파운드)</option>
          <option value="HKD">HKD(홍콩 달러)</option>
          <option value="IDR(100)">IDR(100)(인도네시아 루피아)</option>
          <option value="JPY(100)">JPY(100)(일본 옌)</option>
          <option value="KRW">KRW(한국 원)</option>
          <option value="KWD">KWD(쿠웨이트 디나르)</option>
          <option value="MYR">MYR(말레이지아 링기트)</option>
          <option value="NOK">NOK(노르웨이 크로네)</option>
          <option value="NZD">NZD(뉴질랜드 달러)</option>
          <option value="SAR">SAR(사우디 리얄)</option>
          <option value="SEK">SEK(스웨덴 크로나)</option>
          <option value="SGD">SGD(싱가포르 달러)</option>
          <option value="THB">THB(태국 바트)</option>
          <option value="USD">USD(미국 달러)</option>
        </select>
      </div>
      <div class="card-body">
        <label for="amount" class="form-label fw-bold">환전 금액</label>
        <input type="number" name="" id="amount" class="form-control text-center mb-3" v-model="amount">
        <button class="btn btn-primary fw-bold" @click="exchange">환산</button>
      </div>
      <div class="card-body">
        <label for="result" class="form-label">결과</label>
        <input type="text" id="result" :value="result" class="form-control text-center" disabled>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import axios from 'axios'

const from = ref('')
const to = ref('')
const amount = ref(0)
const result = ref(0)

const getExchangeRate = function() {
  axios.get('http://127.0.0.1:8000/rates/exchange-rate/')
  .then((response) => {
    console.log('환율을 가져왔습니다.')
    console.log(response.data)
  })
  .catch((error) => {
    console.error(error)
  })
}

const changeValue = function() {
  const temp = from.value
  from.value = to.value
  to.value = temp
}

const exchange = function() {
  axios.post('http://127.0.0.1:8000/rates/convert/', {
    amount: amount.value,
    from_currency: from.value,
    to_currency: to.value
  })
  .then((response) => {
    console.log('환전을 완료했습니다.')
    console.log(response.data.result)
    result.value = response.data.result
    if (to.value === 'IDR(100)' || to.value === 'JPY(100)') {
      result.value = (result.value * 100).toFixed(2)
    } else {
      result.value = result.value.toFixed(2)
    }
    result.value = result.value + ' ' + to.value

    to.value = ''
    from.value = ''
    amount.value = 0
  })
  .catch((error) => {
    console.error(error)
  })
}

// 차후에 주석 해제하여 환율을 가져오는 함수 실행
onMounted(() => {
  getExchangeRate()
})
</script>

<style scoped>

</style>