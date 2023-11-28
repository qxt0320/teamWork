<template>
  <div id="app">
    <img src="../images/logo.png" alt="Logo" class="logo" v-if="showLogo">
    <div class="button">
      <button @click="enterGame" v-if="showLogo">进入游戏</button>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      showLogo: true
    };
  },
  created() {
    this.checkRoute();
  },
  watch: {
    '$route'() {
      this.checkRoute();
    }
  },
  methods: {
    enterGame() {
      this.showLogo = false;
      this.$router.push('/shouye');
    },
    checkRoute() {
      if (this.$route.path === '/') {
        this.showLogo = true;
      } else {
        this.showLogo = false;
      }
    }
  }
};
</script>

<style scoped>
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

.logo {
  width: 400px;
  height: 400px;
  position: fixed;
  top: 100px;
}

button {
  margin-top: 300px;
  padding: 10px 50px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
