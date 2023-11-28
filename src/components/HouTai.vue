
<template>
  <div class="container">
    <img src="../images/yonghu.png" alt="Logo" class="logo">
    <div>
      <i class="fa fa-user user-icon"></i>
      <label for="phonenumber" style="padding-left: 30px;">账号：</label>
      <input type="text" v-model="phonenumber" placeholder="请输入账号"><br> <!-- 更新 v-model 绑定 -->
      <i class="fa fa-lock password-icon"></i>
      <label for="password" style="padding-left: 30px;">密码：</label>
      <input type="password" v-model="password" placeholder="请输入密码"><br>
      <button @click="login">登录</button>
      <p v-if="loginError" style="color: red;">{{ loginError }}</p> <!-- 显示登录错误信息 -->
    </div>
    <router-link to="/houtaizhuce">

    </router-link>
  </div>
</template>

<script lang="js">
export default {
  data() {
    return {
      phonenumber: '', // 这里使用 phonenumber 而不是 username
      password: '',
      loginError: '',
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
            phonenumber: this.phonenumber, // API 期望的字段
            password: this.password
          })
        });
        if (response.status === 200) {
          const data = await response.json();
          console.log('Login successful', data);
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', data.userId);
          localStorage.setItem('username', data.username); // 或其他您需要保存的信息
          // 登录成功后的跳转逻辑
          this.$router.push('/home'); // 更改为您的成功路由
        } else {
          const errorData = await response.json();
          this.loginError = errorData.message || '登录失败，请检查手机号和密码';
        }
      } catch (error) {
        this.loginError = '登录请求失败，请检查网络连接';
        console.error('Login failed', error);
      }
    }
  }
};
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
  
  a {
    color: #007bff;
    text-decoration: none;
    margin-top: 20px;
    margin-left: 70px;
  }
  
  button {
    padding: 10px 50px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
    margin-left: 110px;
  }
  
  button:hover {
    background-color: #0056b3;
  }
</style>
