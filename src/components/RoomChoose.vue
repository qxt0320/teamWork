<template>
    <div class="container">
      <a href="http://127.0.0.1:5000">
        <button class="custom-button" @click="type3">
          <img src="../images/threeroom.jpg" alt="" class="ThreeRoom">
        </button>
      </a>

      <a href="http://127.0.0.1:5000">
        <button class="custom-button" @click="type4">
          <img src="../images/fourroom.jpg" alt="" class="FourRoom">
        </button></a>
      </div>
      <div class="music-container">
        <img src="../images/music-off.png" alt="" class="MusicOFF">
        <img src="../images/music-on.png" alt="" class="MusicON">
    </div>
  <img src="../images/IMG_6932.png" alt="" class="img3">
  </template>
  
  <script>
  export default {
    data() {
      return {
        RoomType: '',
      };
    },
    methods: {
      // 3 室
      type3() {
        this.RoomType = 3;
        console.log(this.RoomType)
        this.saveData();
      },
  
      type4() {
        this.RoomType = 4;
        console.log(this.RoomType)
        this.saveData();
      },
  
      saveData() {
        // 使用localStorage保存RoomType的值
        localStorage.setItem('RoomType', this.RoomType);
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