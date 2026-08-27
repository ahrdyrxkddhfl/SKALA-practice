import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'

export function useTemperature(getCelsius) {
  const configStore = useConfigStore()

  // 원본 섭씨 값을 Store의 단위 설정에 맞춰 표시용 값으로 변환.
  const displayTemp = computed(() => {
    const celsius = Number(getCelsius())

    if (configStore.unit === 'fahrenheit') {
      return Math.round((celsius * 9) / 5 + 32)
    }
    return Math.round(celsius)
  })

  const unitSymbol = computed(() => configStore.unitSymbol)
  return { displayTemp, unitSymbol }
}
