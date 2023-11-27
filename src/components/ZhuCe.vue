<template>
  <div class="container">
    <img src="../images/zuche.png" alt="Logo" class="logo">
    <label for="name"> 昵称: </label>
    <input type="text" placeholder="请输入昵称" v-model="name"><br>
    <label for="phone">账号: </label>
    <input type="text" placeholder="请输入账号" v-model="phoneNumber"><br>
    <label for="password">密码: </label>
    <input type="password" placeholder="请输入密码" v-model="password"><br>  
    <router-link to="/SucceedPage">
    <button @click="register">注册</button>  
  </router-link>
  </div>
</template>  
  
<script lang="js">
export default {
  data() {
    return {
      username: '',
      phonenumber: '',
      password: '',
      registerError: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://api2.andylive.cn/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            phonenumber: this.phonenumber,
            password: this.password
          })
        });
        if (response.status === 200) {
          const data = await response.json();
          console.log('Registration successful', data);
          // 保存token、userId和username到本地存储或 Vuex 等状态管理器中
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', data.userId);
          localStorage.setItem('username', data.username);
          // 其他成功逻辑处理
        } else {
          this.registerError = '注册失败，请检查用户名、手机号和密码';
          console.error('Registration failed', error);
          // 其他失败逻辑处理
        }
      } catch (error) {
        this.registerError = '注册失败，请检查用户名、手机号和密码';
        console.error('Registration failed', error);
        // 其他失败逻辑处理
      }
    }
  }
};
</script>
  
<style scoped>  


.container {  

  align-items: center;
  flex-direction: column;
  background-color: rgb(241, 252, 232);

  height: 100vh;
  padding: 250px 250px;
  margin-left: -300px;
  
}

.component {
  width: 200%; /* 增大组件的宽度为容器的两倍 */
  height: 200%; /* 增大组件的高度为容器的两倍 */
}

input {  
margin-bottom: 20px;  
width: 200px;  
padding: 10px;  
}
.logo {  
  width: 500px;  /* 调整宽度和高度 */  
  height: 500px;  /* 调整宽度和高度 */  
  position: absolute;  
  right: 20px;  
  bottom: 20px;  
}  
  

button {  
  padding: 10px 50px;  
  font-size: 16px;  
  background-color: #007bff;  
  color: #fff;  
  border: none;  
  border-radius: 5px;  
  cursor: pointer;
  margin-left: 60px;
}  
  
button:hover {  
  background-color: #0056b3;  
}
  </style>
