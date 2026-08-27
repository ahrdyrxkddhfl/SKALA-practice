import { createRouter, createWebHistory } from 'vue-router'
import WeatherHomeView from '@/views/WeatherHomeView.vue'

const validCityIds = new Set(['city_01', 'city_02', 'city_03', 'city_04', 'city_05'])

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'WeatherHome',
      component: WeatherHomeView,
    },
    {
      path: '/about',
      name: 'WeatherAbout',
      component: () => import('@/views/WeatherAboutView.vue'),
    },
    {
      path: '/weather/:cityId',
      name: 'WeatherDetail',
      component: () => import('@/views/WeatherDetailView.vue'),
    },
    {
      path: '/not-found',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
    },
    {
      path: '/favorite',
      name: 'WeatherFavorite',
      component: () => import('@/views/WeatherFavoriteView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'NotFound' },
    },
  ],
})

// 등록되지 않은 cityId로 상세 화면에 접근하면 404 화면으로 보냅니다.
router.beforeEach((to) => {
  if (to.name === 'WeatherDetail') {
    const cityId = String(to.params.cityId)
    if (!validCityIds.has(cityId)) {
      return { name: 'NotFound' }
    }
  }
})

export default router
