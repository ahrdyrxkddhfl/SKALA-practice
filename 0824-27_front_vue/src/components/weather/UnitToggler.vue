<script setup>
import { useConfigStore } from '@/stores/configStore'

const configStore = useConfigStore()

function handleChange() {
  configStore.toggleUnit()
}
</script>

<template>
  <div class="unit-toggler">
    <span>온도 단위</span>
    <el-switch
      :model-value="configStore.unit === 'fahrenheit'"
      active-text="℉"
      inactive-text="℃"
      @change="handleChange"
    />
  </div>
</template>

<style scoped>
.unit-toggler {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
