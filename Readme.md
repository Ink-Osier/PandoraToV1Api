# 项目简介

为了方便大家将 [Pandora-Next](https://github.com/pandora-next/deploy) 项目与各种其他项目结合完成了本项目。

本项目支持将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/chat/completions` 接口，暂时只支持流式响应，暂未支持非流式响应。

如果本项目对你有帮助的话，请点个小星星吧~

# 更新日志

### 0.0.6

- 修复接入ChatGPT-Next-Web后回复会携带上次的回复的Bug

# 注意

本项目的运行需要 Pandora-Next 开启 `auto_conv_arkose:true`

# 支持的模型

目前支持的模型包括：

1. gpt-4-classic：纯文字生成的 GPT-4，未加入任何插件，对应的是官方的 GPT-4-Classic

2. gpt-4-s：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的默认 GPT-4（绘图的响应有时候有些不稳定）

# Docker-Compose 部署

仓库内已包含相关文件和目录，拉到本地后修改 docker-compose.yml 文件里的环境变量后运行`docker-compose up -d`即可。

# 环境变量说明：

- UPLOAD_BASE_URL 用于dalle模型生成图片的时候展示所用，需要设置为使用如 [ChatGPT-Next-Web](https://github.com/ChatGPTNextWebTeam/ChatGPT-Next-Web) 的用户可以访问到的 Uploader  容器地址，如：http://127.0.0.1:50012

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

## 功能演示

### 联网

![api-1](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/e9a71acf-4804-4280-a774-82e9c0f009a4)

### 代码解释器

![api-2](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/37c0381f-a70a-42bb-83f1-1491053240b7)

### 绘图

![api-3](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/58d140fb-56b2-445c-946d-2d5c5c6a2ec0)
