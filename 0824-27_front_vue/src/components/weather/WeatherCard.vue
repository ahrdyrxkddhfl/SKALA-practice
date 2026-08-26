<script setup>
const props = defineProps({
  cityItem: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['select-card', 'click-detail'])
</script>

<template>
  <article
    class="weather-card"
    @click="emit('select-card', `${props.cityItem.name}이 선택되었습니다.`)"
  >
    <h3>{{ props.cityItem.name }}</h3>
    <p>현재 기온: {{ props.cityItem.temp }}℃</p>
    <p>날씨: {{ props.cityItem.status }}</p>

    <span v-if="props.cityItem.temp >= 25">더움</span>
    <span v-else>선선함</span>

    <button @click.stop="emit('click-detail', props.cityItem.id)">상세보기</button>
  </article>
</template>
