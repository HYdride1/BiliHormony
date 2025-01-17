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

部署：

uvicorn main:app --reload

在给出的网址后加上/docs即可查看自动生成的接口文档

### 测试

安装httpx 和pytest

`pip install httpx`

`pip install pytest`

之后终端运行pytest就可以按照test_main里的测试用例进行测试了,目前每次测试会在测试前重置数据库

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




### 接口描述

#### 用户相关

请求方式均为post

1. 注册：/user/signup
   客户端发送的json格式为

   ```
   {
   "account" :  str
   "password": str
   }
   ```

   返回示例：

   ```json
   {
     "account": "string",
     "password": "string",
     "u_id": 0,
     "like": "",
     "coin": 100
   }
   ```

2. 登录：/user/login
   客户端发送的json格式为

   ```json
   {
     "account": "string",
     "password": "string"
   }
   ```

   返回一个字符串

3. 我的界面中的数据：/user/detail
   客户端发送的json格式为

   ```json
   {
     "account": "string"
   }
   ```

####  视频相关

请求方式均为post

1. 根据bv号返回视频的点赞：/video/like

   服务端返回的json格式为

   ```
   {
   "like": int
   }
   ```

   

2. 根据bv号返回视频的投币：/video/coin

   服务端返回的json格式为

   ```
   {
   "coin": int
   }
   ```

   

3. 热门：/video/hot

   返回值为video的List
   
   video示例：
   
   ```json
   {
     "bv": 0,
     "type": 0,
     "name": "string",
     "like": 0,
     "coin": 0,
     "url": "string",
     "cover_url": "string"
   }
   ```
   
4. 视频名字：/video/name

   客户端发送的json格式为
   
   ```
   {
   "name" :  str
   }
   ```
   
   返回video的List，参考3
   
5. 主页：/video/homepage

   客户端发送的json格式为
   
   ```
   {
   "account" :  str
   }
   ```
   
   返回值为video的List，参考3
   
6. 请求：/video/bv

   客户端发送的json格式为

   ```
   {
   "bv": int
   }
   ```

   返回一个video，参考3

7. 分类：/video/cate

   客户端发送的json格式为
   
   ```
   {
   "cate" :  int
   }
   ```
   
   返回所有类型为cate的视频，返回值为video的List，参考3

TODO：运行日志？

