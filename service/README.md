# 服务端已实现功能
```python
请在每次更新代码功能后更新此文档
接口均已使用apipost测试完成
```
！！！**开发阶段请勿保存重要数据于数据库，每次应用前请删除旧数据库，应用运行后将自动创建数据库**

## 数据库结构
| 表名                | 说明     |
|:------------------|:-------|
| user              | 用户表    |
| rooms             | 房间表    |
| room_participants | 房间参与者表 |

### user表
| 字段名       | 说明   |
|:----------|:-----|
| id        | 用户id |
| username  | 手机号  |
| password  | 密码   |
| real_name | 用户名  |
| score     | 得分   |
| rank      | 排名   |

### rooms表
| 字段名              | 说明   |
|:-----------------|:-----|
| id               | 房间id |
| creator_username | 创建者  |
| participants     |      |
| player1_ready    |      |
| player2_ready    |      |
| player3_ready    |      |

### room_participants表
| 字段名      | 说明   |
|:---------|:-----|
| room_id  | 房间id |
| username | 用户名  |

## 接口部分
### 用户登录
```python
请求地址：/api/login
请求方式：POST
参数：phonenumber, password
```
```
状态码：200
响应示例：
{
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjEzNTk5Nzg5Mzg5IiwiZXhwIjoxNzAwMDEzMzU4fQ.tjyzdnqTchgTOCTibEmwBDO2ncjcPDczU8kAdxDcPRA",
	"userId": 1,
	"username": "13599789389"
}
```

### 用户注册
```python
请求地址：/api/register
请求方式：POST
参数：phonenumber, password, yourname
```
```
状态码：200
响应示例：
{
	"message": "User registered successfully",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjEzNTk5Nzg5MTg5IiwiZXhwIjoxNzAwMDEzNTY2fQ.kYIfNzhr4OLq0HPw9xTYPBUqd33mtd5QFHRaGQLtMmM"
}
```

### 创建房间
```python
请求地址：/api/createroom
请求方式：POST
header：Authorization: Bearer token
参数：RoomID
```
```
状态码：200
响应示例：
{
	"RoomID": "1233"
}
```
```
状态码：409
响应示例：
{
	"error": "RoomID已存在"
}
```

### 加入房间
```python
请求地址：/api/joinroom
请求方式：POST
header：Authorization: Bearer token
参数：RoomID
```
```
状态码：200
响应示例：
{
	"message": "User joined the room successfully"
}
```
```
状态码：400
响应示例：
{
	"message": "User already in the room"
}
```

### 退出房间
```python
请求地址：/api/outroom
请求方式：POST
header：Authorization: Bearer token
参数：RoomID
```
```
状态码：200
响应示例：
{
	"message": "User left the room"
}
```
```
状态码：404
响应示例：
{
	"error": "Room not found"
}
```
```
状态码：403
响应示例：
{
	"error": "User not in room"
}
```

### 准备游戏
```python
请求地址：/api/readygame
请求方式：POST
header：Authorization: Bearer token
参数：RoomID,ReadyStatus
```
```
状态码：200
响应示例：
{
	"message": "Ready status updated successfully"
}
```
