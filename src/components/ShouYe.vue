<template>
  <div class="container">
    <img src="../images/logo.png" alt="Logo" class="logo">
    <h1>抽乌龟</h1>
    <label for="username">账号：</label>
    <input type="text" placeholder="请输入账号" v-model="phonenumber"><br>
    <label for="password">密码：</label>
    <input type="password" placeholder="请输入密码" v-model="password"><br>
    <button @click="login">登录</button>
    <p v-if="loginError">{{ loginError }}</p>
    <router-link to="/zhuce">
      <a href="ZhuCe.vue">新用户注册</a><br>
    </router-link>
  </div>
</template>


<script lang="js">
export default {
  data() {
    return {
      phonenumber: '',
      password: '',
      loginError: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://api2.andylive.cn/api/login', {
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
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', data.userId);
          localStorage.setItem('username', data.username);
          this.$router.push('/GameStart');
        } else {
          const errorData = await response.json();
          this.loginError = '登录失败: ' + errorData.error;
        }
      } catch (error) {
        this.loginError = '登录失败，请检查网络连接';
        console.error('Login error', error);
      }
    }
  }
};
</script>

    
    <style scoped>  

 
    .container {  
      background-color: rgb(241, 252, 232);  
      
    
   position:fixed;
      top:100px;

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