# 项目结构
```
/project_root
├── client/                    # 前端部分
│   ├── __pycache__/           # 编译缓存
│   ├── build/                 # 构建输出
│   ├── dist/                  # 项目分发文件
│   ├── node_modules/          # NPM 依赖
│   ├── public/                # 静态文件
│   ├── src/                   # 源代码
│   │   ├── assets/            # 资源文件
│   │   ├── components/        # Vue 组件
│   │   ├── composables/       # 组合式 API
│   │   ├── router/            # 路由配置
│   │   ├── styles/            # 样式文件
│   │   └── view/              # 视图组件
│   ├── .gitignore             # Git 忽略文件
│   ├── .npmrc                 # NPM 配置
│   ├── index.html             # 入口 HTML 文件
│   ├── package.json           # NPM 项目配置
│   ├── README.md              # 项目说明
│   └── vite.config.ts         # Vite 配置
│
├── resource/                  # 资源文件夹
│
└── server/                    # 后端 FastAPI 部分
│    ├── api/                   # API 路由和业务逻辑
│    ├── component/             # 组件
│    ├── schemas/               # 数据模式定义
│    ├── scripts/               # 脚本
│    ├── utils/                 # 工具类
│    ├── config.py              # 配置文件
│    └── main.py                # FastAPI 入口
│
├── app-dev.py                 # 开发环境配置
├── app.py                     # 主应用文件
├── app.spec                   # 应用规格
├── demo.py                    # 示例代码
├── monitor.py                 # 监控工具
├── requirements.txt           # Python 依赖
├── server.py                  # 服务器启动文件
└── start_app.bat             # 启动脚本
```

# App

![image-20241128172909554](https://cdn.jsdelivr.net/gh/narugakuru/images@master/img/image-20241128172909554.png)

根据json来生成对应的界面，编写json管理脚本参数传入和UI生成

![image-20241128172940481](https://cdn.jsdelivr.net/gh/narugakuru/images@master/img/image-20241128172940481.png)

![image-20241128173409378](https://cdn.jsdelivr.net/gh/narugakuru/images@master/img/image-20241128173409378.png)

