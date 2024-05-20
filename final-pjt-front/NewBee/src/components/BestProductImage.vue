<template>
  <div>
    <div id="carouselExampleControls" class="carousel slide rounded-3 w-100 h-25 mb-4" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
            <img src="@/assets/images/temp1.jpeg" class="d-block w-100" alt="">
        </div>
        <div class="carousel-item">
            <img src="@/assets/images/temp2.jpeg" class="d-block w-100" alt="">
        </div>
        <div class="carousel-item">
            <img src="@/assets/images/temp3.jpeg" class="d-block w-100" alt="...">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
</div>
</template>

<script setup>
</script>

<style scoped>
/* 임시 CSS 차후 변경할 예정 */
img {
  height: 300px;
}
</style>