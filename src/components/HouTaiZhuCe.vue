<template>  
    <div class="container">  

        <img src="../images/yonghu.png" alt="Logo" class="logo">

    
      <div>  
        <i class="fa fa-user user-icon"></i>  
        <label for="username" style="padding-left: 30px;">账号：</label>  
        <input type="text" v-model="username" placeholder="请输入账号"><br>  
        <i class="fa fa-lock password-icon"></i>  
        <label for="password" style="padding-left: 30px;">密码：</label>  
        <input type="password" v-model="password" placeholder="请输入密码"><br>
        <button @click="register">注册</button> <!-- 更新为调用register方法 -->
        <p v-if="registerError" style="color: red;">{{ registerError }}</p>
      </div>  
    </div>  
  </template>

<script lang="js">
export default {
  data() {
    return {
      username: '1', // 如果你的API不需要这个字段，这行可以删除
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
            phonenumber: this.phonenumber,
            password: this.password,
            yourname: this.username // 如果API不需要这个字段，这行可以注释或删除
          })
        });
        if (response.status === 200) {
          const data = await response.json();
          console.log('Registration successful', data);
          localStorage.setItem('token', data.token);
          localStorage.setItem('userId', data.userId);
          // 这里的data.username应根据实际返回的数据结构进行调整
          localStorage.setItem('username', data.username || this.phonenumber);
          this.$router.push('/zhucesucceed'); // 假设您有一个注册成功的路由
        } else {
          const errorData = await response.json();
          this.registerError = errorData.error || '注册失败，请检查信息是否正确';
        }
      } catch (error) {
        this.registerError = '注册请求失败，请检查网络连接';
        console.error('Registration failed', error);
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
