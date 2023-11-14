<!-- src/App.vue -->

<template>
  <div id="app">

    <router-view />
  </div>
</template>

<script>


export default {

};

</script>

<style>
/* 在这里添加全局样式 */
body,
html {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  background-color: rgb(241, 252, 232);
  /* 用你喜欢的颜色替换这里的值 */
  color: #000;
  /* 文本颜色，可以根据背景颜色调整 */
  min-height: 100vh;
  /* 保证最小高度占满整个视口 */
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
