<script setup>
import { ref } from 'vue'

//화면을 먼저 만들기 위해 실제 API 대신 가상 날씨 데이터를 사용.
const weatherList = ref([
    { id: 'city_01', name: '서울', temp: 28, status: '맑음'},
    { id: 'city_02', name: '수원', temp: 24, status: '비'},
    { id: 'city_03', name: '부산', temp: 26, status: '구름'},
    { id: 'city_04', name: '고양', temp: 28, status: '흐림'},
    { id: 'city_05', name: '성남', temp: 29, status: '비'},
])

const searchQuery = ref('')
const selectedCityInfo = ref('카드를 클릭하거나 검색해보세요.')

function showDetail(cityName, status) {
    window.alert(`${cityName}의 현재 날씨는 [${status} 상태입니다.]`)
}
</script>

<template>
    <div class="dashboard-wrapper">
        <section class="search-box">
            <h2>도시 검색</h2>
                <input
                    type="text"
                    :value="searchQuery"
                    placeholder="검색할 도시 이름 입력"
                    @input="searchQuery = $event.target.value"
        </section>

        <section class="list=box">
            <h2>지역별 날씨 현황</h2>

            <article
            v-for="item in weatherList"
            :key="item.id"
            class="weather-card"
            @click="selectedCityInfo = `${item.name}이 선택되었습니다.`"
            >
            <h3>{{ item.name }} ({{ item.status }})</h3>
            <p>현재 기온: {{ item.temp }}℃</p>

            <span v-if="item.temp >= 25">더움</span>
            <span v-else>선선함</span>

            <button @click.stop="showDetail(item.name, item.status")>상세보기</button>
        </article>
        </section>

        <p class="status-bar">{{ selectedCityInfo }}</p>
    </div>
</template>