

<template>
  <div class="start-game-container">
    <img src="../images/logo模糊版.png" alt="" class="logo">
    <div class="title">
      <h1>抽乌龟</h1>
    </div>

    <router-link to="/menu">
      <button @click="startGame" class="start-button">开始游戏</button>
    </router-link>
    <img src="../images/IMG_6937.png" alt="" class="img1">
  </div>
</template>

<script>

export default {
  methods: {
    startGame() {
      // 在这里添加开始游戏的逻辑，可以导航到游戏页面或执行其他操作
      this.$router.push('/menu')
      console.log('游戏已开始！');
    },
    beforeRouteLeave(to, from, next) {
      this.dataToClear = null;
      next();
    },
  },


};
</script>

<style scoped>
/* 在这里添加组件的样式 */
.logo {
  position: absolute;
  width: 300px;
  top: 50px;
  left: 540px;
}

.title {
  position: absolute;
  top: 350px;
  left: 630px;
}

.img1 {
  position: absolute;
  width: 450px;
  left: 850px;
  top: 290px;
}

.start-button {
  position: absolute;
  top: 450px;
  left: 630px;
  background-color: #8ea898;
  color: #000;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
</style>
