<script setup>
import { useConfigStore } from '@/stores/configStore'
const configStore = useConfigStore()
</script>

<template>
  <div>
    <span>현재 단위: {{ configStore.unitSymbol }}</span>
    <button @click="configStore.toggleUnit">단위 변경</button>
  </div>
</template>
