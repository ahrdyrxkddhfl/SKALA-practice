import { createRouter, createWebHistory } from 'vue-router'

/* [요구사항 1] 지연 로딩(Lazy Loading)
 * component에 컴포넌트를 직접 import하지 않고 () => import(...) 화살표 함수를 넣는다.
 * 이렇게 하면 그 경로에 실제로 들어갈 때 비로소 파일을 다운로드한다. */
const routes = [
  {
    path: '/',
    name: 'WeatherHome',
    component: () => import('@/views/WeatherHomeView.vue'),
  },
  {
    // :cityId 는 동적 경로 매칭. /weather/city_01 처럼 들어오면 cityId = 'city_01'
    path: '/weather/:cityId',
    name: 'WeatherDetail',
    component: () => import('@/views/WeatherDetailView.vue'),
  },
  {
    // [요구사항 6] 본인의 추가 view
    path: '/favorite',
    name: 'WeatherFavorite',
    component: () => import('@/views/WeatherFavoriteView.vue'),
  },
  {
    path: '/about',
    name: 'WeatherAbout',
    component: () => import('@/views/WeatherAboutView.vue'),
  },
  {
    /* [요구사항 1] Catch-all Route
     * 위의 어떤 규칙에도 안 걸린 주소를 전부 잡아낸다.
     * 반드시 목록의 '맨 마지막'에 있어야 한다. 위에 두면 모든 주소를 얘가 삼켜버린다. */
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
