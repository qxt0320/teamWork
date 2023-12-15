<template>
  <div class="success-message">
    <div class="icon">&#10004;</div>
    <h1>注册成功！</h1>
    <div class="button-container">
      <router-link to="/shouye">
        <button @click="goToHome">返回</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
div  {
  background-color: rgb(241, 252, 232);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
}

.success-message {
  text-align: center;
}

.icon {
  font-size: 72px;
  vertical-align: middle;
  margin-top: 10px;
}

h1 {
  font-size: 36px;
  display: inline-block;
  vertical-align: middle;
  margin-bottom: 20px;
}

.button-container {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}
</style>
