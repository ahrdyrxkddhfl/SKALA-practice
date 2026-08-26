<script setup>
// RouterLink, RouterView는 app.use(router)로 전역 등록되어 import가 필요 없다
</script>

<template>
  <div class="app-shell">
    <!-- [요구사항 2] Navigation Bar -->
    <nav class="nav-bar">
      <h1 class="nav-title">Weather Dashboard</h1>

      <div class="nav-links">
        <!-- to에 문자열 경로를 주기 -->
        <RouterLink to="/">메인</RouterLink>

        <!-- to에 이름(name)을 주기-->
        <RouterLink :to="{ name: 'WeatherFavorite' }">즐겨찾기</RouterLink>

        <RouterLink to="/about">소개</RouterLink>
      </div>
    </nav>

    <!-- [요구사항 2] 메인 콘텐츠 영역: URL에 매칭된 View가 여기에 꽂힌다 -->
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  max-width: 640px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  color: black;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 14px 18px;
  border: 1px solid grey;
  border-radius: 12px;
  background: whitesmoke;
}

.nav-title {
  margin: 0;
  font-size: 17px;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-links a {
  padding: 6px 12px;
  border: 1px solid gainsboro;
  border-radius: 6px;
  background: white;
  color: black;
  font-size: 13px;
  text-decoration: none;
}

.nav-links a:hover {
  border-color: skyblue;
  color: steelblue;
}

/* 현재 보고 있는 페이지의 링크는 Vue Router가 자동으로 이 클래스를 붙여준다 */
.nav-links a.router-link-active {
  background: steelblue;
  border-color: steelblue;
  color: white;
  font-weight: bold;
}

.content {
  margin-top: 16px;
}
</style>
