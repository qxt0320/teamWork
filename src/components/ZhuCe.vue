<template>
  <div class="container">
    <img src="../images/zuche.png" alt="Logo" class="logo">
    <label for="name">昵称:</label>
    <input type="text" placeholder="请输入昵称" v-model="username"><br> <!-- 昵称输入绑定到 username -->
    <label for="phone">账号:</label>
    <input type="text" placeholder="请输入账号" v-model="phonenumber"><br> <!-- 账号输入绑定到 phonenumber -->
    <label for="password">密码:</label>
    <input type="password" placeholder="请输入密码" v-model="password"><br> <!-- 密码输入绑定到 password -->
    <button @click="register">注册</button> <!-- 点击按钮触发 register 方法 -->
    <p v-if="registerError">{{ registerError }}</p> <!-- 显示注册错误信息 -->
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
        const response = await fetch('http://api2.andylive.cn/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            yourname: this.username,
            phonenumber: this.phonenumber,
            password: this.password
          })
        });
        if (response.status === 200) {
          const data = await response.json();
          console.log('Registration successful', data);
          localStorage.setItem('token', data.token);
          this.$router.push('/SucceedPage');
        } else {
          const errorData = await response.json();
          this.registerError = errorData.message; // 显示具体的错误信息
        }
      } catch (error) {
        this.registerError = '网络错误或服务器不可达';
        console.error('Registration failed', error);
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