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



### 两张表

1. users

   | u_id     | account  | password | like   | coin     |
   | -------- | -------- | -------- | ------ | -------- |
   | Integer  | String   | String   | String | Integer  |
   | 主键     | 唯一     |          |        |          |
   | NOT NULL | NOT NULL | NOT NULL |        | NOT NULL |

   

1. videos

   | bv       | name   | type     | like     | coin     | url      |
   | -------- | ------ | -------- | -------- | -------- | -------- |
   | Integer  | String | Integer  | Interger | Interger | String   |
   | 主键     |        |          |          |          |          |
   | NOT NULL | NOT    | NOT NULL | NOT NULL | NOT NULL | NOT NULL |

   



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

### TODO  视频的URL

1. 视频的点赞：/video/like

   服务端返回的json格式为
   {
   "bv": int

   }

2. 视频的投币：/video/coin

   服务端返回的json格式为
   {

   "account":str

   "bv": int

   }

3. 热门：/video/hot

   服务端返回的json格式为
   {

   "bvs": int[]

   }
   **注：**存疑

4. 视频名字：/video/name

   客户端发送的json格式为
   {
   "name" :  str

   }

   服务端返回的json格式为
   {
   "bv": int

   "name": str

   }

5. 主页：/video/homepage

   客户端发送的json格式为
   {
   "account" :  str

   }

   服务端返回的json格式为
   {
   "bv": int

   "name": str

   }

6. 请求：/video/request

   服务端返回的json格式为
   {

   "bv": int

   }

7. 分类：/video/cate

   客户端发送的json格式为
   {
   "cate" :  int

   }

   服务端返回的json格式为
   {
   "bvs": int[]

   }

8.后端创建视频，接受前端url创建视频？