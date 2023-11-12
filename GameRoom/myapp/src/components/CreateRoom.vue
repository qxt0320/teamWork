<template>
    <div class="create-container">
      <div class="title">房 间 号</div>
  
      <div class="input-row">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
      </div>
  
      <button class="create-button">创建房间</button>
    </div>
    <img src="../images/IMG_6933.png" alt="" class="img2">
  </template>
  
  <script>
  export default {
  
  }
  </script>
  
  <style scoped>
  .create-container {
    display: flex;
    flex-direction: column; /* 更改为纵向排列 */
    align-items: center;
    position: relative;
    text-align: center;
  }
  
  .img2 {
    position: absolute;
    width: 550px;
    height: 500px;
    bottom: 0;
    left: 0;
  }
  
  .title {
    font-size: 75px;
    margin-bottom: 30px;
  }
  
  .input-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
  }
  
  .input-box {
    width: 150px;
    height: 150px;
    font-size: 24px;
    text-align: center;
    border: 2px solid #ccc;
    border-radius: 10px;
    margin: 100px
  }
  
  .create-button {
    font-size: 50px;
    padding: 50px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 50px;
  }
  
  .custom-button {
    border: none;
    background: none;
    cursor: pointer;
    padding: 0;
  }
  </style>
  