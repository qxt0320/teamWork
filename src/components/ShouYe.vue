<template>  
    <div class="container">  
      <img src="../imgaes/logo.png" alt="Logo" class="logo">  
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
    
  <script lang="ts">  
  export default {  
    methods: {  
      login() {  
        // 在这里执行登录逻辑  
        console.log('Login button clicked');  
      }  
    }  
  }  
  </script>  
    
    <style scoped>  

 
    .container {  
      background-color: rgb(241, 252, 232);  
      
    
   
    height: 100vh;
    padding: 20px;
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