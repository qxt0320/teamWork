

<template>
  <div class="menu-container">
    <!-- 加入房间 -->
    <router-link to="/gameroom">
      <button class="custom-button" @click="navigateToGuidePage(2)">
        <img src="../images/Frame 3.png" alt="" class="frame3">
      </button></router-link>
    <!-- 人机对战 -->
    <router-link to="/page1">
      <button class="custom-button" @click="navigateToGuidePage(3)">
        <img src="../images/Frame 4.png" alt="" class="frame4">
      </button></router-link>
    <!-- 新手指南 -->
    <router-link to="/guide">
      <button class="custom-button" @click="navigateToGuidePage(1)">
        <img src="../images/Frame 2.png" alt="" class="frame2">
      </button></router-link>
    <img src="../images/IMG_6934.png" alt="" class="img2">
    <div class="music-container">
      <img src="../images/music-off.png" alt="" class="MusicOFF">
      <img src="../images/music-on.png" alt="" class="MusicON">
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    startGame() {
      // 在这里添加开始游戏的逻辑，可以导航到游戏页面或执行其他操作
      console.log('游戏已开始！');
    },
    beforeRouteLeave(to, from, next) {
      this.dataToClear = null;
      next();
    },
    navigateToGuidePage(buttonNumber) {
      // 在这里你可以执行一些逻辑，然后导航到guide页面
      // 可以根据按钮的不同执行不同的逻辑
      this.$router.push('/guide');
    },
  },


};
</script>

<style scoped>
/* 在这里添加组件的样式 */
.img2 {
  position: absolute;
  width: 300px;
  height: 260px;
  bottom: 0;
  left: 0;
}

.MusicOFF {
  position: absolute;
  width: 100px;
  bottom: 0;
  right: 0;
  cursor: pointer;
}

.MusicON {
  position: absolute;
  width: 100px;
  bottom: 100px;
  right: 0;
  cursor: pointer;
}

.frame4 {
  width: 300px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 20px;
  margin: 80px;
}

.frame3 {
  width: 300px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 20px;
  margin: 80px;
}

.frame2 {
  width: 300px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 20px;
  margin: 80px;
}

.custom-button {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  /* 可以去掉按钮的默认 padding */
}
</style>
