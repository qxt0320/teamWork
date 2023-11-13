<template>
  <div>
    <div class="create-container">
      <div class="title">房 间 号</div>

      <div class="input-row">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
        <input class="input-box" type="text" maxlength="1">
      </div>
      <router-link to="/roomchoose">
        <button class="create-button">创建房间</button></router-link>
    </div>
    <div class="music-container">
      <img src="../images/music-off.png" alt="" class="MusicOFF">
      <img src="../images/music-on.png" alt="" class="MusicON">
    </div>

    <img src="../images/IMG_6933.png" alt="" class="img2">
  </div>
</template>
  
<script>
export default {

}
</script>
  
<style scoped>
.create-container {
  display: flex;
  flex-direction: column;
  /* 更改为纵向排列 */
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
  