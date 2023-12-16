## 项目简介

为了方便大家将 [Pandora-Next](https://github.com/pandora-next/deploy) 项目与各种其他项目结合完成了本项目。

本项目支持将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/chat/completions` 接口，支持流式和非流式响应。

如果本项目对你有帮助的话，请点个小星星吧~

## 更新日志

### 0.1.2

- 紧急修复：GPTS 未携带消息的问题

- 请使用 `0.1.0` 和 `0.1.1` 版本的服务尽快升级！

### 0.1.1

- 支持 `gpt-3.5-turbo` 模型

### 0.1.0

- 重磅更新

- 已支持访问大部分的GPTS

- 注意：本次更新需要更新 `docker-compose.yml` 文件以及 `gpts.json` 文件

### 0.0.11

- 修复一些偶现的bug

### 0.0.10

- 已支持非流式响应

- 更新latest版本镜像

### 0.0.9

- 修复在 ChatGPT-Next-Web 网页端修改请求接口后出现 `Failed to fetch` 报错的问题

### 0.0.8

- 增加了对 GPT-4-Mobile 模型的支持，模型名为 `gpt-4-mobile`

### 0.0.7

- 一定程度上修复图片无法正常生成的问题
- 注意：`docker-compsoe.yml`有更新

### 0.0.6

- 修复接入ChatGPT-Next-Web后回复会携带上次的回复的Bug

## 注意

> [!CAUTION]
> 1. 本项目的运行需要 Pandora-Next 开启 `auto_conv_arkose:true`。
>
> 2. 本项目对话次数对Pandora-Next的对话额度消耗比例为：
>     - `gpt-4-s`、`gpt-4-mobile`、`GPTS`：`1:14`；
>     - `gpt-3.5-turbo`：`1:4`；
>
> 3. 本项目实际为将来自 `/v1/chat/completions` 的请求转发到Pandora-Next的 `/backend-api/conversation` 接口，因此本项目并不支持高并发操作，请不要接入如 `沉浸式翻译` 等高并发项目。
>

## 支持的模型

目前支持的模型包括：

1. gpt-4-s：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的默认 GPT-4（绘图的响应有时候有些不稳定）

2. gpt-4-mobile：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的手机版 GPT-4，截止至2023年12月15日，本模型使用量不计入 GPT-4 用量（即不受每 3 小时 40 次的限制）

3. 几乎所有的 GPTS（配置方式见下文）

4. gpt-3.5-turbo

## Docker-Compose 部署

仓库内已包含相关文件和目录，拉到本地后修改 docker-compose.yml 文件里的环境变量后运行`docker-compose up -d`即可。

## 环境变量说明：

- UPLOAD_BASE_URL：用于dalle模型生成图片的时候展示所用，需要设置为使用如 [ChatGPT-Next-Web](https://github.com/ChatGPTNextWebTeam/ChatGPT-Next-Web) 的用户可以访问到的 Uploader  容器地址，如：http://127.0.0.1:50012

- KEY_FOR_GPTS_INFO：仅获取 GPTS 信息的 key，需要该 key 能够访问所有配置的 GPTS。后续发送消息仍需要在请求头携带请求所用的 key。

## GPTS配置说明

如果需要使用 GPTS，需要修改 `gpts.json` 文件，其中每个对象的key即为调用对应 GPTS 的时候使用的模型名称，而 `id` 则为对应的模型id，该 `id` 对应每个 GPTS 的链接的后缀。配置多个GPTS的时候用逗号隔开。

例如：PandoraNext的官方 GPTS 的链接为：`https://chat.oaifree.com/g/g-CFsXuTRfy-pandoranextzhu-shou`，则该模型的 `id` 的值应为 `g-CFsXuTRfy-pandoranextzhu-shou`，而模型名可以自定义。

示例：

```json
{
    "gpt-4-classic": {
        "id":"g-YyyyMT9XH-chatgpt-classic"
    },
    "pandoraNext":{
        "id":"g-CFsXuTRfy-pandoranextzhu-shou"
    }
}
```

注意：使用该配置的时候需要保证正确填写 `docker-compose.yml` 的环境变量 `KEY_FOR_GPTS_INFO`，同时该变量设置的 `key` 允许访问所有配置的 GPTS。

## 示例

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
      - CUSTOM_MODELS=+gpt-4-s,+gpt-4-mobile,+<gpts.json 中的模型名>

```

## 功能演示

### 联网

![api-1](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/e9a71acf-4804-4280-a774-82e9c0f009a4)

### 代码解释器

![api-2](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/37c0381f-a70a-42bb-83f1-1491053240b7)

### 绘图

![api-3](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/8eea9436-12ee-46b1-86c1-67e7e97da83a)

### GPT-4-Mobile

![api-4](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/2eb4fd4f-7c66-4a1f-a54a-3c280a36e509)

### GPTS

![api-5](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/299df56a-d245-4920-8892-94e1a9cc644a)

## Star 历史

![Stargazers over time](https://api.star-history.com/svg?repos=Ink-Osier/PandoraToV1Api&type=Date)