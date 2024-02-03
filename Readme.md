## 项目简介

> [!IMPORTANT]
>
> Respect Zhile大佬, Respect Pandora！

为了方便大家将 [Pandora-Next](https://github.com/pandora-next/deploy) 项目与各种其他项目结合完成了本项目。

本项目支持：

1. 将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/chat/completions` 接口，支持流式和非流式响应。

2. 将 Pandora-Next  `proxy` 模式下的 `backend-api` 转为 `/v1/images/generations` 接口

如果你想要尝试自己生成Arkose Token从而将PandoraNext的额度消耗降低到`1:4`，你可以看看这个项目：[GenerateArkose](https://github.com/Ink-Osier/GenerateArkose)，但是请注意，**该项目并不保证使用该项目生成的Arkose Token不会封号，使用该项目造成的一切后果由使用者自行承担**。

如果本项目对你有帮助的话，请点个小星星吧~

如果有什么在项目的使用过程中的疑惑或需求，欢迎提 `Issue`，或者加入 Community Telegram Channel: [Inker 的魔法世界](https://t.me/InkerWorld) 来和大家一起交流一下~

## 更新日志

见 `Release` 页面。

## 功能列表

- [x] 支持 代码解释器、联网、绘图

- [x] 支持 gpt-4-s

- [x] 支持 gpt-4-mobile

- [x] 支持 gpt-3.5-turbo

- [x] 支持 gpts

- [x] 支持 流式输出

- [x] 支持 非流式输出

- [x] 支持 dalle 绘图接口

- [x] 支持 接口保活

- [x] 支持 自定义接口前缀

- [x] 支持 日志等级划分

- [x] 支持 gpt-4-vision

- [x] 支持 Bot模式（QQ、微信机器人等建议开启，网页应用请不要开启）

- [x] 支持 指定进程、线程数

- [x] 支持文件生成

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
>
> 5. 提问的艺术：当出现项目不能正常运行时，请携带 `DEBUG` 级别的日志在 `Issue` 或者社区群内提问，否则将开启算命模式~

## 支持的模型

目前支持的模型包括：

1. gpt-4-s：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的默认 GPT-4（绘图的响应有时候有些不稳定）

2. gpt-4-mobile：支持代码解释器、bing联网、dalle绘图的 GPT-4，对应的是官方的手机版 GPT-4，截止至2023年12月15日，本模型使用量不计入 GPT-4 用量（即不受每 3 小时 40 次的限制）

3. 几乎所有的 GPTS（配置方式见下文）

4. gpt-3.5-turbo

## Docker-Compose 部署

仓库内已包含相关文件和目录，拉到本地后修改 docker-compose.yml 文件里的环境变量后运行`docker-compose up -d`即可。

## config.json 变量说明：

- `log_level`: 用于设置日志等级，可选值为：`DEBUG`、`INFO`、`WARNING`、`ERROR`，默认为 `DEBUG`

- `need_log_to_file`: 用于设置是否需要将日志输出到文件，可选值为：`true`、`false`，默认为 `true`，日志文件路径为：`./log/access.log`，默认每天会自动分割日志文件。

- `process_workers`: 用于设置进程数，如果不需要设置，可以保持不变，如果需要设置，可以设置为需要设置的值，如果设置为 `1`，则会强制设置为单进程模式。

- `process_threads`: 用于设置线程数，如果不需要设置，可以保持不变，如果需要设置，可以设置为需要设置的值，如果设置为 `1`，则会强制设置为单线程模式。

- `pandora_base_url`: Pandora-Next 的部署地址，如：`https://pandoranext.com`，注意：不要以 `/` 结尾。可以填写为本项目可以访问到的 PandoraNext 的内网地址。

- `pandora_api_prefix`: PandoraNext Proxy 模式下的 API 前缀

- `backend_container_url`: 用于dalle模型生成图片的时候展示所用，需要设置为使用如 [ChatGPT-Next-Web](https://github.com/ChatGPTNextWebTeam/ChatGPT-Next-Web) 的用户可以访问到的本项目地址，如：`http://1.2.3.4:50011`，同原环境变量中的 `UPLOAD_BASE_URL`

- `backend_container_api_prefix`: 用于设置本项目 `/v1/xxx` 接口的前缀，如果留空则与官方api调用接口一致。设置示例：`666 `

- `key_for_gpts_info`: 仅获取 GPTS 信息的 key，需要该 key 能够访问所有配置的 GPTS。后续发送消息仍需要在请求头携带请求所用的 key，如果未配置该项，请将 `gpts.json` 文件修改为：

```json
{}
```

- `gpt_4_s_new_name`、`gpt_4_mobile_new_name`、`gpt_3_5_new_name`: 用于设置 gpt-4-s、gpt-4-mobile、gpt-3.5-turbo 的模型名称与别名，如果不需要修改，可以保持不变。如果需要修改，每个模型均支持设置多个别名，多个别名之间以英文逗号隔开，例如：`gpt-4-s` 的别名可以设置为 `gpt-4-s,dall-e-3`，这样在调用的时候就可以使用 `gpt-4-s` 或者 `dall-e-3` 来调用该模型。

- `need_delete_conversation_after_response`: 用于设置是否在响应后删除对话，可选值为：`true`、`false`，默认为 `false`，如果设置为 `true`，则会在响应后删除对话，这样可以保证在页面上不会留下通过本项目调用的对话记录.

- `use_oaiusercontent_url`: 是否使用OpenAI官方图片域名，可选值为：`true`、`false`，默认为 `false`，如果设置为 `true`，则会使用OpenAI的图片域名，否则使用 `backend_container_url` 参数的值作为图片域名。如果设置为 `true`，则 `backend_container_url` 可以不填且图片不会下载到image文件夹中。

- `use_pandora_file_server`: 是否使用PandoraNext的文件服务器，可选值为：`true`、`false`，默认为 `true`，如果设置为 `true`，则会从PandoraNext的文件服务器下载图片等文件，否则将直接从openai的文件服务器下载文件。

- `custom_arkose_url`: 是否需要自定义Arkose Token获取地址，可选值为：`true`、`false`，默认为 `false`，如果设置为 `true`，则会使用 `arkose_urls` 参数的值作为Arkose Token获取地址，否则使用默认的PandoraNext Arkose Token获取地址。

- `arkose_urls`: Arkose Token获取地址，如果 `custom_arkose_url` 为 `false`，则该参数无效，如果 `custom_arkose_url` 为 `true`，则该参数必填，且需要填写为可以获取Arkose Token的地址列表，例如：`https://arkose-proxy-1.pandoranext.com/<proxy-prefix>,https://arkose-proxy-2.pandoranext.com/<proxy-prefix>`，支持同时设置多个Arkose Token获取地址，从前往后轮询调用，如果第一个获取失败则自动从第二个获取，以此类推。

- `dalle_prompt_prefix`: 自定义的DALLE接口prompt前缀，可以引导gpt完成绘图任务。

PS. 注意，arkose_urls中的地址需要支持PandoraNext的Arkose Token获取路径与参数，并与PandoraNext的Arkose Token获取接口的响应格式保持一致。

- `bot_mode`

    - `enabled`: 用于设置是否开启 Bot 模式，可选值为：`true`、`false`，默认为 `false`，开启 Bot 模式后，将可以自定义联网插件的引引用、绘图插件的markdown格式的图片以及插件执行过程的输出，仅建议在 QQ、微信机器人等 Bot 项目中开启，网页应用请不要开启。

    - `enabled_markdown_image_output`: 用于设置是否开启 Bot 模式下绘图插件的markdown格式的图片输出，可选值为：`true`、`false`，默认为 `false`，开启后，将会输出markdown格式的图片输出，仅在 `bot_mode.enabled` 为 `true` 时生效。

    - `enabled_plain_image_url_output`: 用于设置是否开启 Bot 模式下绘图插件的纯图片链接（非markdown格式）输出，可选值为：`true`、`false`，默认为 `false`，开启后，将会输出纯图片链接输出，仅在 `bot_mode.enabled` 为 `true` 时生效。注意：与`enabled_markdown_image_output` 同时开启时，只会输出非 markdown 格式的图片。

    - `enabled_bing_reference_output`: 用于设置是否开启 Bot 模式下联网插件的引用输出，可选值为：`true`、`false`，默认为 `false`，开启后，将会输出联网插件的引用，仅在 `bot_mode.enabled` 为 `true` 时生效。

    - `enabled_plugin_output`: 用于设置是否开启 Bot 模式下插件执行过程的输出，可选值为：`true`、`false`，默认为 `false`，开启后，将会输出插件执行过程的输出，仅在 `bot_mode.enabled` 为 `true` 时生效。
  
- `redis`

    - `host`: Redis的ip地址，例如：1.2.3.4，默认是 redis 容器

    - `port`: Redis的端口，默认：6379，如有特殊需求，你可以将此值设置为其他端口

    - `password`: Redis的密码，默认为空，如果你的Redis服务设置了密码，请将其设置为你的密码

    - `db`: Redis的数据库，默认：0，如有特殊需求，你可以将此值设置为其他数据库

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

## 文件识别接口使用说明

调用方式同官方 `gpt-4-vision-preview` API 

接口URI：`/v1/chat/completions`

请求方式：`POST`

请求体格式示例（以 url 形式传入文件）：

```json
{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "这个pdf里写了什么，用中文回复"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bitcoin.org/bitcoin.pdf"
                    }
                }
            ]
        }
    ],
    "stream": false,
    "model": "gpt-4",
    "temperature": 0.5,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1
}
```

请求体示例（以 Base64 形式传入文件）：
```json
{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "这张图里画了什么"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:<mime>;base64,<文件的Base64>"
                    }
                }
            ]
        }
    ],
    "stream": false,
    "model": "gpt-4-s",
    "temperature": 0.5,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1
}
```

`MIME` 支持列表，包括但不限于（如果非列表中的类型会直接转成纯文本txt执行上传操作）：

```
"image/jpeg", "image/webp", "image/png", "image/gif","text/x-php", "application/msword", "text/x-c", "text/html",  "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/json", "text/javascript", "application/pdf", "text/x-java", "text/x-tex", "text/x-typescript", "text/x-sh", "text/x-csharp", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/x-c++", "application/x-latext", "text/markdown", "text/plain", "text/x-ruby", "text/x-script.python"
```

响应体格式示例：

```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "\n```\nopen_url(\"file-xxxxxxx\")\n```\n这个PDF文件是关于比特币的原始论文，名为《比特币：一种点对点的电子现金系统》，作者是中本聪。这篇论文介绍了一种全新的数字货币系统，它不依赖于任何中心化的金融机构。比特币通过一种去中心化的网络和一种称为区块链的技术来维持交易的安全和完整性。这个系统使用数字签名来确认交易，并通过一种被称为工作量证明的机制来防止双重支付。整个系统旨在创建一个安全、去中心化、对用户友好的数字货币。",
                "role": "assistant"
            }
        }
    ],
    "created": 1703063445,
    "id": "chatcmpl-xxxxxxxx",
    "model": "gpt-4",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0
    }
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

### Bot 模式

#### 开启 Bot 模式

![image](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/9c5fd974-58f2-4b96-839d-aef10f7a1cfc)

#### 关闭 Bot 模式

![image](https://github.com/Ink-Osier/PandoraToV1Api/assets/133617214/c1d3457f-b912-4572-b4e0-1118b48102d8)

## 贡献者们

> 感谢所有让这个项目变得更好的贡献者们！

[![Contributors](https://contrib.rocks/image?repo=Ink-Osier/PandoraToV1Api)](https://github.com/Ink-Osier/PandoraToV1Api/graphs/contributors)

## 平台推荐

> [Cloudflare](https://www.cloudflare.com/)

世界领先的互联网基础设施和安全公司，为您的网站提供 CDN、DNS、DDoS 保护和安全性服务，可以帮助你的项目尽可能避免遭受网络攻击或爬虫行为。
[![Cloudflare](https://www.cloudflare.com/img/logo-cloudflare.svg)](https://www.cloudflare.com/)


## Star 历史

![Stargazers over time](https://api.star-history.com/svg?repos=Ink-Osier/PandoraToV1Api&type=Date)