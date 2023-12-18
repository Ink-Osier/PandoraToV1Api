## 项目简介

为了方便大家将 [Pandora-Next](https://github.com/pandora-next/deploy) 项目与各种其他项目结合完成了本项目。

本项目支持：

1. 将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/chat/completions` 接口，支持流式和非流式响应。

2. 将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/images/generations` 接口

如果本项目对你有帮助的话，请点个小星星吧~

## 更新日志

见 `Release` 页面。

## 待实现功能

- [ ] 支持 gpt-4-vision

- [ ] 支持 日志等级划分

- [ ] 支持 接口保活

## 注意

> [!CAUTION]
> 1. 本项目的运行需要 Pandora-Next 开启 `auto_conv_arkose:true`，同时请尽量升级最新版本的 Pandora-Next，以确保支持此功能。
>
> 2. 本项目对话次数对Pandora-Next的对话额度消耗比例为：
>     - `gpt-4-s`、`gpt-4-mobile`、`GPTS`：`1:14`；
>     - `gpt-3.5-turbo`：`1:4`；
>
> 3. 本项目实际为将来自 `/v1/chat/completions` 的请求转发到Pandora-Next的 `/backend-api/conversation` 接口，因此本项目并不支持高并发操作，请不要接入如 `沉浸式翻译` 等高并发项目。
>
> 4. 本项目并不能绕过 OpenAI 和 PandoraNext 官方的限制，只提供便利，不提供绕过。

## 支持的模型

目前支持的模型包括：

1. gpt-4-s：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的默认 GPT-4（绘图的响应有时候有些不稳定）

2. gpt-4-mobile：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的手机版 GPT-4，截止至2023年12月15日，本模型使用量不计入 GPT-4 用量（即不受每 3 小时 40 次的限制）

3. 几乎所有的 GPTS（配置方式见下文）

4. gpt-3.5-turbo

## Docker-Compose 部署

仓库内已包含相关文件和目录，拉到本地后修改 docker-compose.yml 文件里的环境变量后运行`docker-compose up -d`即可。

## 环境变量说明：

- UPLOAD_BASE_URL：用于dalle模型生成图片的时候展示所用，需要设置为使用如 [ChatGPT-Next-Web](https://github.com/ChatGPTNextWebTeam/ChatGPT-Next-Web) 的用户可以访问到的 Uploader  容器地址，如：http://1.2.3.4:50011

- KEY_FOR_GPTS_INFO：仅获取 GPTS 信息的 key，需要该 key 能够访问所有配置的 GPTS。后续发送消息仍需要在请求头携带请求所用的 key，如果未配置该项，请将 `gpts.json` 文件修改为：

```json
{}
```

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

## 绘图接口使用说明

接口URI：`/v1/images/generations`

请求方式：`POST`

请求头：正常携带 `Authorization` 和 `Content-Type` 即可，`Authorization` 的值为 `Bearer <Pandora-Next 的 fk>`，`Content-Type` 的值为 `application/json`

请求体格式示例：

```json
{
    "model": "gpt-4-s",
    "prompt": "A cute baby sea otter"
}
```

请求体参数说明：

- model：模型名称，需要支持绘图功能，否则绘图结果将为空

- prompt：绘图的 Prompt

响应体格式示例：

```json
{
    "created": 1702788293,
    "data": [
        {
            "url": "http://<upload 容器公网ip>:50012/images/image_20231217044452.png"
        }
    ],
    "reply": "\n```\n{\"size\":\"1024x1024\",\"prompt\":\"A cute baby sea otter floating on its back in calm, clear waters. The otter has soft, fluffy brown fur, and its small, round eyes are shining brightly. It's holding a small starfish in its tiny paws. The sun is setting in the background, casting a golden glow over the scene. The water reflects the colors of the sunset, with gentle ripples around the otter. There are a few seagulls flying in the distance under the pastel-colored sky.\"}Here is the image of a cute baby sea otter floating on its back."
}
```

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