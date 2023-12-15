

<template>
  <div>
    <div class="custom-button">

      <img src="../images/guide.jpg" alt="" class="guide">
    </div>
    <img src="../images/IMG_6932.png" alt="" class="img3">
    <router-link to="/menu">
      <button class="custom-button" @click="navigateToGuidePage(1)">
        <img src="../images/QQ图片20231028222956.png" alt="" class="img4">
      </button></router-link>
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
.guide {
  position: absolute;
  width: 900px;
  top: 50%;
  /* 将顶部偏移设置为50% */
  left: 50%;
  /* 将左侧偏移设置为50% */
  transform: translate(-50%, -50%);
  /* 使用transform属性进行居中 */
}

.img3 {
  position: absolute;
  width: 250px;
  bottom: 0;
  left: 0;
}

.img4 {
  position: absolute;
  width: 150px;
  bottom: 0;
  right: 0;
}

.custom-button {


  display: inline-block;
  /* 行内块元素 */
  cursor: pointer;
}


</style>
<!-- APS-ujiephwRZVsM4qCLchXGwiT56qhwBFXi -->