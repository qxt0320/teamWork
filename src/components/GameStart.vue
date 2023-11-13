

<template>
  <div>
    <div class="start-game-container">
      <img src="../images/logo模糊版.png" alt="" class="logo">
      <div class="title">
        <h1>抽乌龟</h1>
      </div>

      <router-link to="/menu">
        <button @click="startGame" class="start-button">开始游戏</button>
      </router-link>

    </div>
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
.start-game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  text-align: center;
}

.logo {

  width: 300px;
}

.title {
  font-size: 20px;

}

.img1 {
  position: absolute;
  width: 500px;
  bottom: 0;
  right: 0;
  cursor: pointer;
}

.start-button {
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
