<script setup>
import { ref } from 'vue'

const isWarning = ref(false)      // 객체 바인딩용 스위치
const themeClass = ref('bg-dark') // 배열 바인딩용 고정 클래스
</script>

<template>
  <div class="practice-section">
    <h2>v-bind 디렉티브 고급 (클래스 바인딩)</h2>

    <h3>클래스 바인딩 (객체 형식)</h3>
    <p :class="{ 'text-danger': isWarning }">현재 경고 상태: {{ isWarning }}</p>
    <button @click="isWarning = !isWarning">경고 상태 토글</button>
    <br />

    <h3>클래스 바인딩 (배열 형식)</h3>
    <div :class="[themeClass, isWarning ? 'text-danger' : 'text-safe']">
      배열 형식 바인딩 결과
    </div>
  </div>
</template>

<style scoped>
.text-danger {
  color: #e74c3c;
  font-weight: bold;
}
.text-safe {
  color: #2ecc71;
}
.bg-dark {
  background-color: #34495e;
  padding: 10px;
  border-radius: 5px;
}
</style>