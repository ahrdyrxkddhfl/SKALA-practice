<script setup>
const handleLink = () => {
  alert('수식어 덕분에 네이버로 이동하지 않고 함수만 실행됩니다!')
}
const handleBox = () => {
  alert('부모 박스가 클릭되었습니다!')
}
const handleChild1 = () => {
  alert('1번 자식 클릭!')
}
const handleChild2 = () => {
  alert('2번 자식(나만 켜짐) 클릭!')
}
const handleOnce = () => {
  alert('이 알림은 딱 한 번만 뜹니다!')
}
const handleSelf = () => {
  alert('배경(self)을 직접 클릭했습니다!')
}
</script>

<template>
  <div class="practice-section">
    <h2>이벤트 수식어(Modifiers) 학습</h2>

    <h3>1) .prevent — 기본 동작 막기</h3>
    <a href="https://www.naver.com" @click.prevent="handleLink">네이버 링크</a>

    <h3>2) .stop — 버블링 막기</h3>
    <div @click="handleBox" style="padding: 20px; background-color: #eee">
      <p>부모 영역 (클릭 시 alert 발동)</p>
      <button @click="handleChild1">버블링 발생 버튼</button>
      <button @click.stop="handleChild2">버블링 차단 버튼</button>
    </div>

    <h3>3) .once — 한 번만 실행</h3>
    <button @click.once="handleOnce">여러 번 눌러보세요</button>

    <h3>4) .self — 자기 자신 클릭할 때만</h3>
    <div @click.self="handleSelf" style="padding: 30px; background-color: #d5f5e3">
      회색 배경(여기 직접 클릭 → 실행)
      <button>이 버튼 클릭 → 실행 안 됨</button>
    </div>
  </div>
</template>