import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', () => {
  //여러 화면에서 공유할 온도 단위를 상태로 보관.
  const unit = ref('celsius')

  //현재 상태에 맞는 단위 기호 계산.
  const unitSymbol = computed(() => (unit.value === 'celsius' ? '°C' : '°F'))

  //버튼 클릭 시 섭씨와 화씨를 서로 전환.
  function toggleUnit() {
    unit.value = unit.value === 'celsius' ? 'fahrenheit' : 'celsius'
  }

  return { unit, unitSymbol, toggleUnit }
})
