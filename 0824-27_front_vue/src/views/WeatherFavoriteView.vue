<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchWeatherList } from '@/services/weatherApi'
import { useFavoriteStore } from '@/stores/favoriteStore.js'
import BaseDashboardCard from '@/components/weather/BaseDashboardCard.vue'
import WeatherCard from '@/components/weather/WeatherCard.vue'

const router = useRouter()
const favoriteStore = useFavoriteStore()

const weatherList = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

// 즐겨찾기한 도시만 걸러낸다.
const favoriteWeatherList = computed(() =>
  weatherList.value.filter((city) => favoriteStore.isFavorite(city.id)),
)

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

function goDetail(cityId) {
  router.push({ name: 'WeatherDetail', params: { cityId } })
}
</script>

<template>
  <div>
    <BaseDashboardCard>
      <template #title
        ><h2>☆ 즐겨찾기한 도시 ({{ favoriteStore.favoriteCount }}개)</h2></template
      >

      <p v-if="isLoading">날씨 정보를 불러오는 중입니다...</p>
      <p v-else-if="errorMessage">{{ errorMessage }}</p>
      <template v-else>
        <WeatherCard
          v-for="city in favoriteWeatherList"
          :key="city.id"
          :city-item="city"
          @click-detail="goDetail"
        />
        <p v-if="favoriteWeatherList.length === 0">
          아직 즐겨찾기한 도시가 없습니다. 메인에서 ☆ 버튼을 눌러보세요.
        </p>
      </template>
    </BaseDashboardCard>
  </div>
</template>
