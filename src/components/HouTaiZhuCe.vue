<template>  
    <div class="container">  
        <img src="../imgaes/yonghu.png" alt="Logo" class="logo">  
    
      <div>  
        <i class="fa fa-user user-icon"></i>  
        <label for="username" style="padding-left: 30px;">账号：</label>  
        <input type="text" v-model="username" placeholder="请输入账号"><br>  
        <i class="fa fa-lock password-icon"></i>  
        <label for="password" style="padding-left: 30px;">密码：</label>  
        <input type="password" v-model="password" placeholder="请输入密码"><br>  
        <router-link to="/zhucesucceed">
        <button @click="login">注册</button>  
    </router-link>
      </div>  
    </div>  
  </template>  
    
  <script>  
  export default {  
    data() {  
      return {  
        username: '',  
        password: '',  
        userImage: 'yonghu.png',  
        userImageAlt: '描述图片的文字',  
        registerURL: 'houtai1.html'  
      }  
    },  
    methods: {  
      login() {  
        // 在这里添加登录逻辑。可以使用 this.username 和 this.password 来获取输入的值。例如，你可以将这些值发送到后端服务器，或者存储在本地存储中等等。  
      }  
    }  
  }  
  </script>
  <style>

  .my-image {
    width: 80px;
    height: auto; /* 保持宽高比 */
    text-align: center;
    margin-left: 700px;
  }
  
  .container {
    margin-left: 600px;
    align-items: center;
    margin-left: 600px;
    flex-direction: column;
    margin-top: 200px;
  }
  
  .logo {
    width: 100px;
    height: 100px;
    margin-bottom: 20px;
    margin-left: 130px;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
    margin-top: 0;
  }
  
  input {
    margin-bottom: 20px;
    width: 200px;
    padding: 10px;
  }
  

  button {
    margin-left: 50px;
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