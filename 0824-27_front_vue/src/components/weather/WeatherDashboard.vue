<script setup>
import { computed, ref, watch } from 'vue'
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'
import { useRouter } from 'vue-router'
import FilterBar from './FilterBar.vue'
const router = useRouter()

function goDetail(cityId) {
  router.push({ name: 'WeatherDetail', params: { cityId } })
}
//화면을 먼저 만들기 위해 실제 API 대신 가상 날씨 데이터를 사용.
const weatherList = ref([
  {
    id: 'city_01',
    name: '서울',
    temp: 28,
    status: '맑음',
    humidity: 12,
    dust: 12,
    favorite: false,
  },
  { id: 'city_02', name: '수원', temp: 24, status: '비', humidity: 88, dust: 78, favorite: false },
  {
    id: 'city_03',
    name: '부산',
    temp: 26,
    status: '구름',
    humidity: 40,
    dust: 91,
    favorite: false,
  },
  {
    id: 'city_04',
    name: '고양',
    temp: 28,
    status: '흐림',
    humidity: 80,
    dust: 50,
    favorite: true,
  },
  { id: 'city_05', name: '성남', temp: 29, status: '비', humidity: 92, dust: 20, favorite: true },
])

const searchQuery = ref('')
const selectedCityInfo = ref('도시 카드를 선택해보세요.')

const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()
  // 검색어가 없으면 전체 목록을 그대로 반환합니다.
  if (!query) return weatherList.value
  return weatherList.value.filter((city) => city.name.includes(query))
})

const favoriteCount = computed(() => {
  return weatherList.value.filter((city) => city.favorite).length
})

const showFavoriteOnly = ref(false)
const visibleWeatherList = computed(() => {
  if (!showFavoriteOnly.value) return filteredWeatherList.value
  return filteredWeatherList.value.filter((city) => city.favorite)
})

const badDustCount = computed(() => {
  return visibleWeatherList.value.filter((city) => city.dust >= 81).length
})

watch(selectedCityInfo, (message) => console.log('[watch]', message))
watch(favoriteCount, (newCount, oldCount) => {
  console.log(`즐겨찾기 개수 변경: ${oldCount}개 -> ${newCount}개`)
})

function toggleFavorite(city) {
  city.favorite = !city.favorite
}
</script>

<template>
  <div>
    <BaseDashboardCard>
      <template #title><h2>도시 검색</h2></template>
      <SearchBar :current-query="searchQuery" @update-query="(value) => (searchQuery = value)" />
      <FilterBar
        :show-favorite-only="showFavoriteOnly"
        :favorite-count="favoriteCount"
        :bad-dust-count="badDustCount"
        @update-favorite-only="(value) => (showFavoriteOnly = value)"
      />
    </BaseDashboardCard>

    <BaseDashboardCard>
      <template #title><h2>지역별 날씨 현황</h2></template>
      <WeatherCard
        v-for="city in visibleWeatherList"
        :key="city.id"
        :city-item="city"
        @select-card="(message) => (selectedCityInfo = message)"
        @click-detail="goDetail"
        @toggle-favorite="toggleFavorite"
      />
      <p v-if="visibleWeatherList.length === 0">검색 결과가 없습니다.</p>
    </BaseDashboardCard>

    <p class="status-bar">{{ selectedCityInfo }}</p>
  </div>
</template>
