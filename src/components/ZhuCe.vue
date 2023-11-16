<template>  
  <div class="container">  
    <img src="../imgaes/zuche.png" alt="Logo" class="logo">  
    <label for="name"> 昵称:</label>  
    <input type="text" placeholder="请输入昵称" v-model="name"><br>  
    <label for="phone">手机号: </label>  
    <input type="text" placeholder="请输入手机号" v-model="phoneNumber"><br>  
    <label for="password">密码:</label>  
    <input type="password" placeholder="请输入密码" v-model="password"><br>  
    <router-link to="/SucceedPage">
    <button @click="register">注册</button>  
  </router-link>
  </div>  
</template>  
  
<script>  
export default {  
  data() {  
    return {  
      phoneNumber: '',  
      password: ''  
    }  
  },  
  methods: {  
    register() {  
      // 在这里添加注册逻辑  
      // 可以使用 this.phoneNumber 和 this.password 来获取输入的值  
      // 例如，你可以将这些值发送到后端服务器，或者存储在本地存储中等等。  
    }  
  }  
}  
</script>  
  
<style scoped>  


.container {  

  align-items: center;
  flex-direction: column;
  background-color: rgb(241, 252, 232);

  height: 100vh;
  padding: 250px 450px;
 
  
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
}  
  
button:hover {  
  background-color: #0056b3;  
}
  </style>