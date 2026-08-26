<script setup>
import { computed, ref, watch } from 'vue'
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function goDetail(cityId) {
  router.push({ name: 'WeatherDetail', params: { cityId } })
}
//화면을 먼저 만들기 위해 실제 API 대신 가상 날씨 데이터를 사용.
const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음' },
  { id: 'city_02', name: '수원', temp: 24, status: '비' },
  { id: 'city_03', name: '부산', temp: 26, status: '구름' },
  { id: 'city_04', name: '고양', temp: 28, status: '흐림' },
  { id: 'city_05', name: '성남', temp: 29, status: '비' },
])

const searchQuery = ref('')
const selectedCityInfo = ref('도시 카드를 선택해보세요.')

const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()
  // 검색어가 없으면 전체 목록을 그대로 반환합니다.
  if (!query) return weatherList.value
  return weatherList.value.filter((city) => city.name.includes(query))
})

watch(selectedCityInfo, (message) => console.log('[watch]', message))
</script>

<template>
  <div>
    <BaseDashboardCard>
      <template #title><h2>도시 검색</h2></template>
      <SearchBar :current-query="searchQuery" @update-query="(value) => (searchQuery = value)" />
    </BaseDashboardCard>

    <BaseDashboardCard>
      <template #title><h2>지역별 날씨 현황</h2></template>
      <WeatherCard
        v-for="city in filteredWeatherList"
        :key="city.id"
        :city-item="city"
        @select-card="(message) => (selectedCityInfo = message)"
        @click-detail="goDetail"
      />
      <p v-if="filteredWeatherList.length === 0">검색 결과가 없습니다.</p>
    </BaseDashboardCard>

    <p class="status-bar">{{ selectedCityInfo }}</p>
  </div>
</template>
