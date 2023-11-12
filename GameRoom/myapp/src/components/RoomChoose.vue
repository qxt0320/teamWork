<template>
    <div class="container">
      <router-link to="/gameplay">
        <button class="custom-button" @click="navigateToGuidePage(1)">
          <img src="../images/threeroom.jpg" alt="" class="ThreeRoom">
        </button></router-link>
  
      <router-link to="/gameplay">
        <button class="custom-button" @click="navigateToGuidePage(3)">
          <img src="../images/fourroom.jpg" alt="" class="FourRoom">
        </button></router-link>
      </div>
      <div class="music-container">
        <img src="../images/music-off.png" alt="" class="MusicOFF">
        <img src="../images/music-on.png" alt="" class="MusicON">
    </div>
  <img src="../images/IMG_6932.png" alt="" class="img3">
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
        this.$router.push('/gameroom');
      },
    },
  
  
  };
  </script>
  
  <style scoped>
  .container {
    display: flex; /* 启用Flexbox布局 */
    justify-content: space-between; /* 可以根据需要调整对齐方式 */
    position: relative;
    text-align: center; /* 水平居中文本 */
  }
  
  /* 其他样式保持不变 */
  .img3 {
    position: absolute;
      width: 500px;
      height: 500px;
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
  .ThreeRoom {
    width: 400px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    margin-top: 20px;
    margin: 50px;
  }
  
  
  .FourRoom {
    width: 400px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    margin-top: 20px;
    margin: 50px;
  }
  
  .custom-button {
    border: none;
    background: none;
    cursor: pointer;
    padding: 0;
    /* 可以去掉按钮的默认 padding */
  }
  </style>