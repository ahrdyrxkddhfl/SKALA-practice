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
</template>
