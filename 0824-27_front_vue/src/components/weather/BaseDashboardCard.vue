<template>
  <section class="dashboard-card">
    <header v-if="$slots.title" class="dashboard-card__title">
      <slot name="title" />
    </header>

    <slot />
  </section>
</template>

<style scoped>
.dashboard-card {
  margin-bottom: 16px;
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  background: #ffffff;
}

.dashboard-card__title {
  margin-bottom: 12px;
}
</style>
