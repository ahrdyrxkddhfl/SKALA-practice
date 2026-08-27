<script setup>
import { computed, onMounted, ref, watch, watchEffect } from 'vue'
import { fetchWeatherList } from '@/services/weatherApi'
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'
import { useRouter } from 'vue-router'
import FilterBar from './FilterBar.vue'
import { useFavoriteStore } from '@/stores/favoriteStore.js'

const router = useRouter()
const favoriteStore = useFavoriteStore()

function goDetail(cityId) {
  router.push({ name: 'WeatherDetail', params: { cityId } })
}
//화면을 먼저 만들기 위해 실제 API 대신 가상 날씨 데이터를 사용.
const weatherList = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

const searchQuery = ref('')
const selectedCityInfo = ref('도시 카드를 선택해보세요.')

const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()
  // 검색어가 없으면 전체 목록을 그대로 반환합니다.
  if (!query) return weatherList.value
  return weatherList.value.filter((city) => city.name.includes(query))
})

const showFavoriteOnly = ref(false)
const visibleWeatherList = computed(() => {
  if (!showFavoriteOnly.value) return filteredWeatherList.value
  return filteredWeatherList.value.filter((city) => favoriteStore.isFavorite(city.id))
})

const badDustCount = computed(() => {
  return visibleWeatherList.value.filter((city) => city.dust >= 81).length
})

async function loadWeather() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    weatherList.value = await fetchWeatherList()
  } catch (error) {
    console.error(error)
    errorMessage.value = '날씨 정보를 불러오지 못했습니다. API Key와 네트워크 상태를 확인하세요.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadWeather)

watch(selectedCityInfo, (message) => console.log('[watch]', message))
watch(
  () => favoriteStore.favoriteCount,
  (newCount, oldCount) => {
    console.log(`[watch] 즐겨찾기 개수 변경: ${oldCount}개 -> ${newCount}개`)
  },
)
watchEffect(() => {
  console.log('[watchEffect] 검색어:', searchQuery.value)
})
</script>

<template>
  <div>
    <BaseDashboardCard>
      <template #title><h2>도시 검색</h2></template>
      <SearchBar :current-query="searchQuery" @update-query="(value) => (searchQuery = value)" />
      <FilterBar
        :show-favorite-only="showFavoriteOnly"
        :favorite-count="favoriteStore.favoriteCount"
        :bad-dust-count="badDustCount"
        @update-favorite-only="(value) => (showFavoriteOnly = value)"
      />
    </BaseDashboardCard>

    <BaseDashboardCard>
      <template #title><h2>지역별 날씨 현황</h2></template>
      <p v-if="isLoading">날씨 정보를 불러오는 중입니다...</p>
      <p v-else-if="errorMessage">{{ errorMessage }}</p>
      <template v-else>
        <WeatherCard
          v-for="city in visibleWeatherList"
          :key="city.id"
          :city-item="city"
          @select-card="(message) => (selectedCityInfo = message)"
          @click-detail="goDetail"
        />
        <p v-if="visibleWeatherList.length === 0">검색 결과가 없습니다.</p>
      </template>
    </BaseDashboardCard>

    <p class="status-bar">{{ selectedCityInfo }}</p>
  </div>
</template>
