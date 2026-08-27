<script setup>
import { useTemperature } from '@/composables/useTemperature.js'
import DustBadge from './DustBadge.vue'
import { useFavoriteStore } from '@/stores/favoriteStore.js'

const props = defineProps({
  cityItem: { type: Object, required: true },
})

const emit = defineEmits(['select-card', 'click-detail'])

// 부모가 넘겨준 섭씨 값을 composable에 전달.
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
    <p v-if="props.cityItem.tomorrowMax !== null">
      내일: {{ props.cityItem.tomorrowMin }}°C ~ {{ props.cityItem.tomorrowMax }}°C
    </p>

    <div class="card-row">
      <DustBadge :dust="props.cityItem.dust" />

      <el-tag v-if="props.cityItem.temp >= 25" type="danger">더움</el-tag>
      <el-tag v-else type="primary">선선함</el-tag>

      <el-button type="primary" size="small" @click.stop="emit('click-detail', props.cityItem.id)">
        상세보기
      </el-button>

      <el-button size="small" @click.stop="favoriteStore.toggleFavorite(props.cityItem.id)">
        {{ favoriteStore.isFavorite(props.cityItem.id) ? '★ 해제' : '☆ 즐겨찾기' }}
      </el-button>
    </div>
  </article>
</template>

<style scoped>
.card-row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 10px;
}
</style>
