<script setup>
defineProps({
  showFavoriteOnly: { type: Boolean, required: true },
  favoriteCount: { type: Number, required: true },
  badDustCount: { type: Number, required: true },
})

const emit = defineEmits(['update-favorite-only'])
</script>

<template>
  <div class="filter-bar">
    <label>
      <input
        type="checkbox"
        :checked="showFavoriteOnly"
        @change="emit('update-favorite-only', $event.target.checked)"
      />
      즐겨찾기만 보기 ({{ favoriteCount }}개)
    </label>

    <span v-if="badDustCount > 0" class="warn">미세먼지 나쁨 {{ badDustCount }}곳</span>
  </div>
</template>

<style scoped>
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  font-size: 13px;
}
.warn {
  color: orangered;
  font-weight: bold;
}
</style>
