<template>
  <!-- Join组件，用于输入房间号并加入游戏 -->
  <div class="join-container">
    <!-- 标题 -->
    <div class="title">房 间 号</div>

    <div class="input-row">
      <!-- 使用 v-model 进行双向数据绑定 -->
      <input v-model="inputData[0]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[1]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[2]" class="input-box" type="text" maxlength="1">
      <input v-model="inputData[3]" class="input-box" type="text" maxlength="1">
    </div>

    <!-- 进入房间按钮 -->

      <button @click="saveData" class="join-button">进入房间</button>
      <p v-if="joinRoomError">{{ joinRoomError }}</p>
  </div>

  <!-- 音乐控制容器 -->
  <div class="music-container">
    <img src="../images/music-off.png" alt="" class="MusicOFF">
    <img src="../images/music-on.png" alt="" class="MusicON">
  </div>

  <!-- 图片元素 -->
  <img src="../images/IMG_6933.png" alt="" class="img2">
</template>


<script>
export default {
  data() {
    return {
      inputData: ['', '', '', ''],
      joinRoomError: '', // 用于存储加入房间错误信息
    };
  },
  methods: {
    async saveData() {
      const RoomID = this.inputData.join('');
      const token = localStorage.getItem('token'); // 从 localStorage 获取 Token
      if (!token) {
        this.joinRoomError = '未授权访问，请先登录';
        return;
      }

      try {
        const response = await fetch('http://api2.andylive.cn/api/joinroom', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            RoomID: RoomID
          })
        });

        if (response.status === 200) {
          // 成功加入房间，处理成功逻辑，例如跳转到游戏页面
          this.$router.push('/gameplay');
        } else {
          const errorData = await response.json();
          this.joinRoomError = errorData.message || '加入房间失败';
        }
      } catch (error) {
        this.joinRoomError = '网络错误或服务器不可达';
        console.error('Error joining room', error);
      }
    },
  },
};
</script>


  
  <style scoped>
  .join-container {
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
    margin: 100px
  }
  
  .join-button {
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
  