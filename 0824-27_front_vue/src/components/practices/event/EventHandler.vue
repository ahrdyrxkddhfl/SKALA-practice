<script setup>
import { ref } from 'vue'

const count = ref(0)

// 메서드 핸들러 함수 정의
const showAlert = () => {
  alert('함수가 성공적으로 호출되었습니다!')
}
</script>

<template>
  <div class="practice-section">
    <h2>v-on 이벤트 핸들링 기초</h2>

    <h3>1) 인라인 핸들러 (Inline Handler)</h3>
    <p>현재 카운트: {{ count }}</p>
    <button @click="count++">1씩 증가</button>

    <h3>2) 메서드 핸들러 (Method Handler)</h3>
    <button @click="showAlert">알림창 띄우기</button>
  </div>
</template>