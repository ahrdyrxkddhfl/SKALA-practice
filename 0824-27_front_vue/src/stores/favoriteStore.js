import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useFavoriteStore = defineStore('favorite', () => {
  const favoriteIds = ref([])

  const favoriteCount = computed(() => favoriteIds.value.length)

  function isFavorite(cityId) {
    return favoriteIds.value.includes(cityId)
  }

  function toggleFavorite(cityId) {
    if (isFavorite(cityId)) {
      favoriteIds.value = favoriteIds.value.filter((id) => id !== cityId)
    } else {
      favoriteIds.value.push(cityId)
    }
  }

  return { favoriteIds, favoriteCount, isFavorite, toggleFavorite }
})
