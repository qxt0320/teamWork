<template>
  <div class="create-container">
    <!-- 房间号标题 -->
    <div class="title">房 间 号</div>

    <!-- 输入框行 -->
    <div class="input-row">
      <!-- 使用 v-model 进行双向数据绑定 -->
      <input v-model="inputData[0]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[1]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[2]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[3]" class="input-box" type="text" maxlength="1">
    </div>

    <!-- 点击按钮时触发 saveData 方法 -->
    <router-link to="/roomchoose">
      <button @click="saveData" class="create-button">创建房间</button>
    </router-link>
  </div>

  <!-- 音乐容器 -->
  <div class="music-container">
    <img src="../images/music-off.png" alt="" class="MusicOFF">
    <img src="../images/music-on.png" alt="" class="MusicON">
  </div>

  <!-- 图片 -->
  <img src="../images/IMG_6933.png" alt="" class="img2">
</template>

<script>
export default {
  data() {
    return {
      inputData: ['', '', '', ''], // 初始化为四个空字符串
    };
  },
  methods: {
    saveData() {
      // 将 inputData 数组连接成字符串并赋值给 RoomID
      this.RoomID = this.inputData.join('');
      
      // 在这里可以处理保存数据的逻辑，例如将数据发送到服务器或在本地存储中保存
      console.log('Saved Data:', this.RoomID);
    },
  },
};
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
  margin: 100px;
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
