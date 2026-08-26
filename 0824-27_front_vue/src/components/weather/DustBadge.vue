<script setup>
defineProps({
  dust: {
    type: Number,
    required: true,
  },
})
</script>

<template>
  <span v-if="dust >= 81" class="badge bad">미세먼지 나쁨</span>
  <span v-else-if="dust >= 31" class="badge soso">미세먼지 보통</span>
  <span v-else class="badge good">미세먼지 좋음</span>
</template>

<style scoped>
.badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  color: white;
}
.bad {
  background: darkgray;
}
.soso {
  background: orange;
}
.good {
  background: greenyellow;
}
</style>
