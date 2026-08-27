<script setup>
const props = defineProps({
  currentQuery: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update-query'])
</script>

<template>
  <input
    type="text"
    :value="props.currentQuery"
    placeholder="검색할 도시 이름 입력"
    @input="emit('update-query', $event.target.value)"
  />
  <p class="search-echo">
    검색 중인 도시: <strong>{{ props.currentQuery }}</strong>
  </p>
</template>

<style scoped>
.status-bar {
  padding: 12px;
  border-radius: 8px;
  background: #f0f9eb;
  text-align: center;
}
</style>

<style scoped>
.search-bar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-echo {
  margin: 0;
  font-size: 13px;
  color: darkgray;
}
</style>
