<script setup>
import { ref } from 'vue'

/* ==================================================================
 * [요구사항 1] 배열 렌더링용 원본 데이터
 * [요구사항 5] 교재 기본 3개(서울/수원/부산) + 본인 추가(고양(본가)/성남(for skala))
 *              + 본인 추가 필드: humidity(습도), dust(미세먼지), favorite
 *
 * ref()로 감싼 배열은 내부 객체 속성까지 깊게(deep) 반응형으로 변환된다.
 * 따라서 city.favorite 처럼 개별 속성만 바꿔도 화면이 다시 그려진다.
 * ================================================================== */
const weatherList = ref([
  { id: 'city_01', name: '서울', temp: 28, status: '맑음', humidity: 45, dust: 32, favorite: false },
  { id: 'city_02', name: '수원', temp: 24, status: '비',   humidity: 82, dust: 18, favorite: false },
  { id: 'city_03', name: '부산', temp: 26, status: '구름', humidity: 61, dust: 55, favorite: false },
  { id: 'city_04', name: '고양', temp: 22, status: '흐림', humidity: 70, dust: 91, favorite: true },
  { id: 'city_05', name: '성남', temp: 29, status: '흐림', humidity: 85, dust: 12, favorite: true  },
])

// [요구사항 3] 검색창에 입력된 도시 이름
const searchQuery = ref('')

// [요구사항 4] 화면 하단 상태바 문구
const statusMessage = ref('카드를 클릭하거나 검색해 보세요.')

/* ------------------------------------------------------------------
 * [요구사항 3] 한글(IME) 대응 입력 핸들러
 *
 * v-model은 한글 조합 중(초성+중성을 조립하는 단계)에는 값 갱신을
 * 건너뛰도록 설계되어 있어 실시간 검색에 부적합하다.
 * v-model 대신 :value + @input 을 직접 연결하면
 * 조합 중인 글자(ㅅ → 서 → 설 → 서울)까지 즉시 반영된다.
 * ------------------------------------------------------------------ */
const handleSearchInput = (event) => {
  searchQuery.value = event.target.value
}

// [요구사항 4-1] 카드 클릭 -> 상태바 문구 갱신
const selectCard = (cityName) => {
  statusMessage.value = `${cityName}이(가) 선택되었습니다.`
}

/* [요구사항 4-2] 상세보기 -> alert 표시
 * 버블링 차단은 template의 @click.stop 수식어가 담당한다. */
const showDetail = (cityName, status) => {
  window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다.`)
}

/* [요구사항 5 추가] 즐겨찾기 토글
 * 인자로 받은 city는 weatherList 내부의 원본 객체를 참조하므로
 * 속성을 직접 바꾸면 반응형 시스템이 감지해 화면을 갱신한다. */
const toggleFavorite = (city) => {
  city.favorite = !city.favorite
  statusMessage.value = city.favorite
    ? `⭐ ${city.name}을(를) 즐겨찾기에 추가했습니다.`
    : `☆ ${city.name}을(를) 즐겨찾기에서 해제했습니다.`
}
</script>

<template>
  <div class="weather-app">
    <h2 class="app-title">과제 1: 날씨 (Mockup)</h2>

    <!-- 검색 박스 -->
    <section class="panel">
      <h3 class="panel-title">도시 검색</h3>

        <!-- [요구사항 3] v-model 대신 :value + @input (한글 실시간 반영) -->
      <input
        type="text"
        class="search-input"
        placeholder="검색할 도시 이름 입력"
        :value="searchQuery"
        @input="handleSearchInput"
      />

      <p class="search-result">
        검색된 도시: <strong>{{ searchQuery || '(입력 없음)' }}</strong>
      </p>
    </section>

    <!-- 지역별 날씨 현황 -->
    <section class="panel">
      <h3 class="panel-title">지역별 날씨 현황</h3>

      <!-- [요구사항 1] v-for + :key 필수 / [요구사항 4-1] 카드 클릭 -->
      <div
        v-for="city in weatherList"
        :key="city.id"
        class="weather-card"
        @click="selectCard(city.name)"
      >
        <div class="card-info">
          <p class="city-name">
            {{ city.name }} ({{ city.status }})
            <!-- [요구사항 5 추가] 즐겨찾기 별표 -->
            <span v-if="city.favorite">⭐</span>
          </p>

          <p class="city-detail">
            현재 기온: {{ city.temp }}°C &nbsp;·&nbsp; 습도: {{ city.humidity }}%
          </p>

          <div class="badge-row">
            <!-- [요구사항 2] 기온 조건부 라벨 (v-if / v-else) -->
            <span v-if="city.temp >= 25" class="badge badge-hot">더움 (25도 이상)</span>
            <span v-else class="badge badge-cool">선선함 (25도 미만)</span>

            <!-- [요구사항 5 추가] 미세먼지 3단계 (v-if / v-else-if / v-else) -->
            <span v-if="city.dust >= 81" class="badge badge-bad">미세먼지 나쁨</span>
            <span v-else-if="city.dust >= 31" class="badge badge-soso">미세먼지 보통</span>
            <span v-else class="badge badge-good">미세먼지 좋음</span>
          </div>
        </div>

        <div class="card-actions">
          <!-- [요구사항 4-2] .stop 으로 버블링 차단 -> 카드 클릭 이벤트 미발동 -->
          <button class="btn" @click.stop="showDetail(city.name, city.status)">
            상세보기
          </button>

          <!-- [요구사항 5 추가] 여기도 .stop 필수 -->
          <button class="btn btn-fav" @click.stop="toggleFavorite(city)">
            {{ city.favorite ? '★ 해제' : '☆ 즐겨찾기' }}
          </button>
        </div>
      </div>
    </section>

    <!-- 상태바 -->
    <footer class="status-bar">{{ statusMessage }}</footer>
  </div>
</template>

<style scoped>
.weather-app {
  max-width: 560px;
  margin: 24px auto;
  padding: 20px;
  border: 1px solid grey;
  border-radius: 12px;
  background: whitesmoke;
  font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  color: black;
}

.app-title {
  margin: 0 0 20px;
  font-size: 20px;
  border-bottom: 2px solid black;
  padding-bottom: 10px;
}

.panel {
  margin-bottom: 20px;
}

.panel-title {
  font-size: 15px;
  color: black;
  margin: 0 0 10px;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid grey;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}
.search-input:focus {
  border-color: blue;
}

.search-result {
  margin: 10px 0 0;
  font-size: 13px;
  color: darkgray;
}

/* 날씨 카드 */
.weather-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 14px;
  margin-bottom: 10px;
  border: 1px solid grey;
  border-radius: 8px;
  background: ivory;
  cursor: pointer;
  transition: all 0.2s;
}
.weather-card:hover {
  border-color: skyblue;
  box-shadow: 0 2px 10px rgba(64, 158, 255, 0.15);
}

.city-name {
  margin: 0 0 4px;
  font-weight: bold;
  font-size: 15px;
}

.city-detail {
  margin: 0 0 8px;
  font-size: 13px;
  color: darkgray;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
  color: white;
}
.badge-hot  { background: deeppink; }
.badge-cool { background: skyblue; }
.badge-bad  { background: grey; }
.badge-soso { background: burlywood}
.badge-good { background: yellowgreen; }

.card-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.btn {
  padding: 6px 12px;
  border: 1px solid grey;
  border-radius: 6px;
  background: #fff;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
}
.btn:hover {
  border-color:skyblue;
  color: skyblue;
}
.btn-fav:hover {
  border-color: orange;
  color: orange;
}

/* 상태바 */
.status-bar {
  padding: 12px;
  border-radius: 8px;
  background: lightgoldenrodyellow;
  border: 1px solid ivory;
  color: black;
  font-size: 13px;
  text-align: center;
}
</style>