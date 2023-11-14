

<template>
  <div>
    <div class="custom-button">

      <img src="../images/IMG_6956.png" alt="" class="guide">
      <span class="button-text"> 游戏由一名玩家开始，逆时针轮流进行，在你的回合中，可以从下一位玩家手中抽一张牌。<br>
        你的目标是凑成一对相同的牌，并且将对牌打出。<br>
        牌堆中会有一张乌龟牌，这张牌不能与其他牌凑成一对，如果场上只剩下乌龟牌，拥有乌龟牌的玩家将输掉比赛。<br>
        功能牌<br>
        转向牌<br>
        可以改变抽牌方向，由逆时针转为顺时针方向；<br>
        交换牌<br>
        可以与指定玩家进行卡牌的交换，对方无法拒绝。<br>
        抽完牌后，需要等待5s下家的行为，下家可以决定是否需要锁定此牌，如果有此行为，上家5s之后可以决定重新抽取其他牌或仍然选择这张牌。</span>
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

.button-text {
  position: absolute;
  bottom: 50%;
  /* 将底部偏移设置为50% */
  left: 50%;
  /* 将左侧偏移设置为50% */
  transform: translate(-50%, 50%);
  /* 使用transform属性进行居中 */
  color: black;
  font-size: 20px;
  font-weight: bold;
  font-family: 'Your-Font-Family', sans-serif;
}
</style>
<!-- APS-ujiephwRZVsM4qCLchXGwiT56qhwBFXi -->