<script setup>
import { ref } from 'vue'

const fontSize = ref(16)
const textColor = ref('#2c3e50')

// 스타일 객체 통째로 바인딩
const styleObject = ref({
  color: '#ffffff',
  backgroundColor: '#8e44ad',
  padding: '15px',
  borderRadius: '8px',
})

const extraStyle = ref({
  fontStyle: 'italic',
  letterSpacing: '2px',
})
</script>

<template>
  <div class="practice-section">
    <h2>v-bind 디렉티브 고급 (스타일 바인딩)</h2>

    <h3>1) 객체 형식 (인라인 직접 작성)</h3>
    <p :style="{ fontSize: fontSize + 'px', color: textColor }">글자 크기: {{ fontSize }}px</p>
    <button @click="fontSize += 2">키우기</button>&nbsp;
    <button @click="fontSize -= 2">줄이기</button>&nbsp;
    <button @click="textColor = '#e74c3c'">빨갛게</button>

    <h3>2) 객체 형식 (변수 통째로 바인딩)</h3>
    <p :style="styleObject">스타일 객체를 변수로 분리한 경우</p>

    <h3>3) 배열 형식 (여러 스타일 객체 병합)</h3>
    <p :style="[styleObject, extraStyle]">두 스타일 객체가 병합된 결과</p>
  </div>
</template>
