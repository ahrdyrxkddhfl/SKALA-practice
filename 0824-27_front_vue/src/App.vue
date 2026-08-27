<script setup>
import { provide } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import UnitToggler from './components/weather/UnitToggler.vue'

provide('appTitle', 'Vue Weather Dashboard')
</script>

<template>
  <div class="app-container">
    <header>
      <h1>Vue Weather Dashboard</h1>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/favorite">즐겨찾기</RouterLink>
      </nav>
      <UnitToggler />
    </header>

    <RouterView />
  </div>
</template>

<style scoped>
nav {
  display: flex;
  gap: 12px;
  margin: 8px 0;
}
</style>
