<script setup>
import { inject } from 'vue'

// App.vue에서 provide한 값을 중간 컴포넌트 전달 없이 직접 받습니다.
const appTitle = inject('appTitle', 'Weather Dashboard')
</script>

<template>
  <section>
    <h2>서비스 소개</h2>
    <p>
      <strong>{{ appTitle }}</strong
      >는 Vue 3 학습을 위한 실습 프로젝트입니다.
    </p>
    <p>Vue Router, Pinia, Axios, Element Plus를 하나의 SPA에서 연결합니다.</p>
  </section>
</template>
