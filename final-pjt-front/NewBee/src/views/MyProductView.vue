<template>
  <div class="text-center">
    <div v-for="(product, index) in userProduct" :key="product.id">
      <h4>{{ index + 1 }}</h4>
      <h5>상품 종류: {{ product.product_type }}</h5>
      <h5>가입날짜: {{ product.join_date }}</h5>
      <div>
        <canvas :id="'rateChart-' + index"></canvas>
      </div>
      <button class="mb-5 btn btn-primary fw-bold" v-if="(product.product_type === '적금') || (product.product_type === '정기예금')"
        @click="getDetail(product, index)">상품 정보 그래프</button>
      <!-- <button class=" mb-3" @click="goDetail(product.deposit_product)">상세 페이지</button> -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { Chart, registerables } from 'chart.js'
import router from '@/router';

Chart.register(...registerables)

const store = useCounterStore()
const getMyProduct = store.getMyProduct
const userProduct = store.userProduct

onMounted(() => {
  getMyProduct()
})

const getDetail = async (product, index) => {
  let data = null;
  let product_title = '';

  if (product.product_type === '정기예금') {
    await store.getDepositDetail(product.deposit_product);
    data = store.depositDetail.deposit_options;
    product_title = store.depositDetail.fin_prdt_nm;
  } else if (product.product_type === '적금') {
    await store.getSavingDetail(product.saving_product);
    data = store.savingsDetail.saving_options;
    product_title = store.savingsDetail.fin_prdt_nm;
  }

  if (data) {
    const ctx = document.getElementById('rateChart-' + index).getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(item => item.save_trm + '개월'),
        datasets: [
          {
            label: '기본 금리',
            data: data.map(item => item.intr_rate),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          },
          {
            label: '우대 금리',
            data: data.map(item => item.intr_rate2),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: product_title,
            font: {
              size: 30 // 원하는 크기로 설정하세요
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: '저축 기간 (개월)'
            }
          },
          y: {
            title: {
              display: true,
              text: '금리 (%)'
            },
            beginAtZero: true
          }
        }
      }
    });
  }
}

// const goDetail = function (id) {
//   router.push({ name: 'depositDetail' }, params: { id: id })
// }
</script>

<style scoped>
canvas {
  width: 800px;
  margin: 0 auto;
}
</style>