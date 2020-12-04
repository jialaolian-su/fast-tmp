# 实现细节

## 使用openapi
### 开发阶段
1. 通过openapi的工具函数```App().openapi()```中的```get_openapi()```把路由生成为可以给前端调用的json
2. 对返回的数据增加接口类型和接口位置，增加额外的css位置等信息
3. 前端通过工具，把后端返回的json数据转化为html页面，并可以自行修改css和相关的工具内容
4. 开发阶段使用后端及时返回的json进行前端页面构建

### 生产阶段

1. 项目打包的时候，前端先通过工具把json格式生成的页面固定为静态非json生成的页面。
2. 前端将项目打包
3. 后端动态生成路由