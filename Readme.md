# 项目简介

为了方便大家将 (Pandora-Next)[https://github.com/pandora-next/deploy] 项目与各种其他项目结合完成了本项目。

# Docker-Compose 部署

仓库内已包含相关文件和目录，拉到本地后修改 docker-compose.yml 文件里的环境变量后运行`docker-compose up -d`即可。

# 环境变量说明：

- UPLOAD_BASE_URL 用于dalle模型生成图片的时候展示所用，需要设置为使用如chatgpt-next-web的用户可以访问到的 Uploader  容器地址，如：http://127.0.0.1:50012

# 示例

以ChatGPT-Next-Web项目的docker-compose部署为例，这里提供一个简单的部署配置文件示例：

```
version: '3'
services:
  chatgpt-next-web:
    image: yidadaa/chatgpt-next-web
    ports:
      - "50013:3000"
    environment:
      - OPENAI_API_KEY=<Pandora-Next 的 fk>
      - BASE_URL=<backend-to-api容器地址>
      - CUSTOM_MODELS=+gpt-4-s,+gpt-4-classic

```