<script setup>
defineProps({
  dust: {
    type: Number,
    required: true,
  },
})
</script>

<template>
  <el-tag v-if="dust >= 81" type="danger">미세먼지 나쁨</el-tag>
  <el-tag v-else-if="dust >= 31" type="warning">미세먼지 보통</el-tag>
  <el-tag v-else type="success">미세먼지 좋음</el-tag>
</template>

<style scoped>
.el-tag {
  font-weight: bold;
}
</style>
