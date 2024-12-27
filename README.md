#### README

安装依赖：

`pip install fastapi "uvicorn[standard]"`

`pip install python-dotenv`

`pip install sqlalchemy`

`pip install pymysql`



.env中的{}内容改成本地数据库的内容

来自：
https://medium.com/@iambkpl/setup-fastapi-and-sqlalchemy-mysql-986419dbffeb





还需要安装这三个库
`pip install python-multipart`

`pip install PyJWT`

`pip install passlib`

实现了用户的相关功能，建好了数据库serverside，并建好了表users

完成了鉴权机制，密码加密存储



### 测试

安装依赖：

pip install httpx

pip install pytest

完成后在终端输入pytest运行测试即可，每次运行测试都会清空并重置一次数据库

测试用例及函数在test_main文件中

测试方式参考：https://fastapi.tiangolo.com/zh/tutorial/testing/#_5

### 两张表

1. users

   | u_id     | account  | password | like   | coin     |
   | -------- | -------- | -------- | ------ | -------- |
   | Integer  | String   | String   | String | Integer  |
   | 主键     | 唯一     |          |        |          |
   | NOT NULL | NOT NULL | NOT NULL |        | NOT NULL |

   

1. videos



### 用户的URL

1. 注册：/user/signup
   客户端发送的json格式为
   {
   "account" :  str
   "password": str

   }

2. 登录：/user/login
   客户端发送的data格式为
   {
   "account" :  str
   "password": str

   }

3. 我的界面中的数据：/user/detail
   客户端发送的json格式为
   {
   "account" :  str

   }

   服务端发送的格式为
   {
   "like": str

   "coin": int

   }