import axios from 'axios'

const API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY

const weatherClient = axios.create({
  baseURL: 'https://api.openweathermap.org/data/2.5/weather',
  timeout: 7000,
})

const airClient = axios.create({
  baseURL: 'https://api.openweathermap.org/data/2.5/air_pollution',
  timeout: 7000,
})

const CITY_LIST = [
  { id: 'city_01', name: '서울', lat: 37.5665, lon: 126.978 },
  { id: 'city_02', name: '수원', lat: 37.2636, lon: 127.0286 },
  { id: 'city_03', name: '부산', lat: 35.1796, lon: 129.0756 },
  { id: 'city_04', name: '고양', lat: 37.6584, lon: 126.832 },
  { id: 'city_05', name: '성남', lat: 37.42, lon: 127.1265 },
]

function assertApiKey() {
  if (!API_KEY) {
    throw new Error('VITE_OPENWEATHER_API_KEY가 설정되지 않았습니다.')
  }
}
async function requestWeather(city) {
  assertApiKey()

  const { data } = await weatherClient.get('', {
    params: {
      lat: city.lat,
      lon: city.lon,
      appid: API_KEY,
      units: 'metric',
      lang: 'kr',
    },
  })

  return data
}

// 미세먼지(PM10) 수치를 가져온다. 실패해도 화면이 죽지 않도록 0을 반환.
async function requestDust(city) {
  try {
    const { data } = await airClient.get('', {
      params: { lat: city.lat, lon: city.lon, appid: API_KEY },
    })
    return data.list?.[0]?.components?.pm10 ?? 0
  } catch (error) {
    console.error('미세먼지 조회 실패:', error)
    return 0
  }
}

const STATUS_MAP = {
  온흐림: '흐림',
  튼구름: '구름 많음',
  실비: '가랑비',
  악천후: '폭풍',
}

function normalizeWeather(city, data, dust) {
  const raw = data.weather?.[0]?.description ?? '정보 없음'
  return {
    id: city.id,
    name: city.name,
    temp: data.main.temp,
    status: STATUS_MAP[raw] ?? raw,
    humidity: data.main.humidity,
    wind: data.wind.speed,
    dust,
  }
}
export async function fetchWeatherList() {
  return Promise.all(
    CITY_LIST.map(async (city) => {
      const [data, dust] = await Promise.all([requestWeather(city), requestDust(city)])
      return normalizeWeather(city, data, dust)
    }),
  )
}

export async function fetchWeatherDetail(cityId) {
  const city = CITY_LIST.find((item) => item.id === cityId)
  if (!city) return null

  const [data, dust] = await Promise.all([requestWeather(city), requestDust(city)])
  return normalizeWeather(city, data, dust)
}
