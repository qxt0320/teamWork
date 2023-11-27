<template>  
    <div class="container">  
      <img src="../images/logo.png" alt="Logo" class="logo">  
      <h1>抽乌龟</h1>  
      <label for="username">账号：</label>  
      <input type="text" placeholder="请输入账号"><br>  
      <label for="password">密码：</label>  
      <input type="password" placeholder="请输入密码"><br>  
      <router-link to="/zhuce">
      <a href="zhuce.html">新用户注册</a><br>  
     
      
    </router-link>
    <button @click="login">登录</button>  
    </div>  
  </template>  
    
    <script lang="js">
    export default {
  data() {
    return {
      phonenumber: '',
      password: '',

    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://api2.andylive.cn', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            phonenumber: this.phonenumber,
            password: this.password
          })
        });
        if (response.status === 200) {
          const data = await response.json();
          console.log('Login successful', data);
          // 保存token、userId和username到本地存储或 Vuex 等状态管理器中
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', data.userId);
          localStorage.setItem('username', data.username);
          // 其他成功逻辑处理
        } else {
          this.loginError = '登录失败，请检查用户名和密码';
          console.error('Login failed', error);
          // 其他失败逻辑处理
        }
      } catch (error) {
        this.loginError = '登录失败，请检查用户名和密码';
        console.error('Login failed', error);
        // 其他失败逻辑处理
      }
    }
  }
};
    </script>
    
    <style scoped>  

 
    .container {  
      background-color: rgb(241, 252, 232);  
      
    
   
    height: 100vh;
    padding: 50px;
        text-align: center;   
      
    }  
    

    .logo {  
        width: 200px;  
        height: 200px;  
        margin-bottom: 20px;  
       
    }  
    h1 {   
        font-size: 24px;  
        margin-bottom: 20px;  
        
    }  
    input {  
        margin-bottom: 10px;  
        width: 200px;  
        padding: 10px;  
        
    }  
    a {   
        color: #007bff;  
        text-decoration: none;  
        margin-top: 20px;  
       
    }  
    button {  
        padding: 10px 50px;  
        font-size: 16px;  
        background-color: #007bff;  
        color: #fff;  
        border: none;  
        border-radius: 5px;  
        cursor: pointer;  
    }  
    button:hover {  
        background-color: #0056b3; 

    }  
   
</style>
