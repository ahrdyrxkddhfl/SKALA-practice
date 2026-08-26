<script setup>
import { ref } from 'vue'

const message = ref('현재 서버 상태 정상')
const userCount = ref(150)
</script>

<template>
  <div class="base-card">
    <h3>하위 컴포넌트 (Child)</h3>
    <slot :text="message" :count="userCount">
      <p>부모가 마크멍븡ㄹ 주입하지 않았을 때으 디폴트 화면</p>
    </slot>
  </div>
</template>
