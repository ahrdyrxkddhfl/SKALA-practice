<script setup>
import { useTemperature } from '@/composables/useTemperature.js'
import DustBadge from './DustBadge.vue'
import { useFavoriteStore } from '@/stores/favoriteStore.js'

const props = defineProps({
  cityItem: { type: Object, required: true },
})

const emit = defineEmits(['select-card', 'click-detail'])

//부모가 넘겨준 섭씨 값을 composable에 전달.
const { displayTemp, unitSymbol } = useTemperature(() => props.cityItem.temp)

const favoriteStore = useFavoriteStore()
</script>

<template>
  <article
    class="weather-card"
    @click="emit('select-card', `${props.cityItem.name}이 선택되었습니다.`)"
  >
    <h3>{{ props.cityItem.name }}</h3>
    <p>현재 기온: {{ displayTemp }}{{ unitSymbol }}</p>
    <p>날씨: {{ props.cityItem.status }}</p>
    <p>습도: {{ props.cityItem.humidity }}%</p>
    <DustBadge :dust="props.cityItem.dust" />

    <span v-if="props.cityItem.temp >= 25">더움</span>
    <span v-else>선선함</span>

    <button @click.stop="emit('click-detail', props.cityItem.id)">상세보기</button>
    <button @click.stop="favoriteStore.toggleFavorite(props.cityItem.id)">
      {{ favoriteStore.isFavorite(props.cityItem.id) ? '★ 해제' : '☆ 즐겨찾기' }}
    </button>
  </article>
</template>

<style scoped>
.weather-card {
  margin: 12px 0;
  padding: 16px;
  border: 1px solid gainsboro;
  border-radius: 8px;
}
</style>
