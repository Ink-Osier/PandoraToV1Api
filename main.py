# 导入所需的库
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS, cross_origin
import requests
import uuid
import json
import time
import os
from datetime import datetime
from PIL import Image
import io
import re

def generate_unique_id(prefix):
    # 生成一个随机的 UUID
    random_uuid = uuid.uuid4()
    # 将 UUID 转换为字符串，并移除其中的短横线
    random_uuid_str = str(random_uuid).replace('-', '')
    # 结合前缀和处理过的 UUID 生成最终的唯一 ID
    unique_id = f"{prefix}-{random_uuid_str}"
    return unique_id


def get_accessible_model_list():
    return [config['name'] for config in gpts_configurations]


def find_model_config(model_name):
    for config in gpts_configurations:
        if config['name'] == model_name:
            return config
    return None

# 从 gpts.json 读取配置
def load_gpts_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 根据 ID 发送请求并获取配置信息
def fetch_gizmo_info(base_url, proxy_api_prefix, model_id):
    url = f"{base_url}/{proxy_api_prefix}/backend-api/gizmos/{model_id}"
    headers = {
        "Authorization": f"Bearer {KEY_FOR_GPTS_INFO}"
    }

    response = requests.get(url, headers=headers)
    # print(f"fetch_gizmo_info_response: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

gpts_configurations = [
    {
        "name":"gpt-4-s"
    },
    {
        "name":"gpt-4-mobile"
    },
    {
        "name":"gpt-3.5-turbo"
    }
]

# 将配置添加到全局列表
def add_config_to_global_list(base_url, proxy_api_prefix, gpts_data):
    global gpts_configurations
    # print(f"gpts_data: {gpts_data}")
    for model_name, model_info in gpts_data.items():
        # print(f"model_name: {model_name}")
        # print(f"model_info: {model_info}")
        model_id = model_info['id']
        gizmo_info = fetch_gizmo_info(base_url, proxy_api_prefix, model_id)
        if gizmo_info:
            gpts_configurations.append({
                'name': model_name,
                'id': model_id,
                'config': gizmo_info
            })

def generate_gpts_payload(model, messages):
    model_config = find_model_config(model)
    if model_config:
        gizmo_info = model_config['config']
        gizmo_id = gizmo_info['gizmo']['id']
        
        payload = {
            "action": "next",
            "messages": messages,
            "parent_message_id": str(uuid.uuid4()),
            "model": "gpt-4-gizmo",
            "timezone_offset_min": -480,
            "history_and_training_disabled": False,
            "conversation_mode": {
                "gizmo": gizmo_info,
                "kind": "gizmo_interaction",
                "gizmo_id": gizmo_id
            },
            "force_paragen": False,
            "force_rate_limit": False
        }
        return payload
    else:
        return None

# 创建 Flask 应用
app = Flask(__name__)
CORS(app, resources={r"/images/*": {"origins": "*"}})

# 添加环境变量配置
BASE_URL = os.getenv('BASE_URL', '')
PROXY_API_PREFIX = os.getenv('PROXY_API_PREFIX', '')
UPLOAD_BASE_URL = os.getenv('UPLOAD_BASE_URL', '')
KEY_FOR_GPTS_INFO = os.getenv('KEY_FOR_GPTS_INFO', '')

VERSION = '0.1.4'
UPDATE_INFO = '合并了 Upload 容器和 Backend 容器'

with app.app_context():
    # 输出版本信息
    print(f"==========================================")
    print(f"Version: {VERSION}")
    print(f"Update Info: {UPDATE_INFO}")


    if not BASE_URL:
        raise Exception('BASE_URL is not set')
    else:
        print(f"BASE_URL: {BASE_URL}")
    if not PROXY_API_PREFIX:
        raise Exception('PROXY_API_PREFIX is not set')
    else:
        print(f"PROXY_API_PREFIX: {PROXY_API_PREFIX}")
    
    print(f"==========================================")

    print(f"GPTS 配置信息")

    # 加载配置并添加到全局列表
    gpts_data = load_gpts_config("./gpts.json")
    add_config_to_global_list(BASE_URL, PROXY_API_PREFIX, gpts_data)
    # print("当前可用GPTS：" + get_accessible_model_list())
    # 输出当前可用 GPTS name
    print(f"当前可用 GPTS 列表: {get_accessible_model_list()}")

    print(f"==========================================")

    # print(f"GPTs Payload 生成测试")

    # print(f"gpt-4-classic: {generate_gpts_payload('gpt-4-classic', [])}")


# 定义获取 token 的函数
def get_token():
    url = f"{BASE_URL}/{PROXY_API_PREFIX}/api/arkose/token"
    payload = {'type': 'gpt-4'}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        return None

import os



# 定义发送请求的函数
def send_text_prompt_and_get_response(messages, api_key, stream, model):
    url = f"{BASE_URL}/{PROXY_API_PREFIX}/backend-api/conversation"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    formatted_messages = []
    for message in messages:
        message_id = str(uuid.uuid4())
        formatted_message = {
            "id": message_id,
            "author": {"role": message.get("role")},
            "content": {"content_type": "text", "parts": [message.get("content")]},
            "metadata": {}
        }
        formatted_messages.append(formatted_message)

    payload = {}

    print(f"model: {model}")
    if model == 'gpt-4-s':
        payload = {
            # 构建 payload
            "action": "next",
            "messages": formatted_messages,
            "parent_message_id": str(uuid.uuid4()),
            "model":"gpt-4",
            "timezone_offset_min": -480,
            "suggestions":[],
            "history_and_training_disabled": False,
            "conversation_mode":{"kind":"primary_assistant"},"force_paragen":False,"force_rate_limit":False
        }
    elif model == 'gpt-4-mobile':
        payload = {
            # 构建 payload
            "action": "next",
            "messages": formatted_messages,
            "parent_message_id": str(uuid.uuid4()),
            "model":"gpt-4-mobile",
            "timezone_offset_min": -480,
            "suggestions":["Give me 3 ideas about how to plan good New Years resolutions. Give me some that are personal, family, and professionally-oriented.","Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.","Design a database schema for an online merch store.","Compare Gen Z and Millennial marketing strategies for sunglasses."],
            "history_and_training_disabled": False,
            "conversation_mode":{"kind":"primary_assistant"},"force_paragen":False,"force_rate_limit":False
        }
    elif model =='gpt-3.5-turbo':
        payload = {
            # 构建 payload
            "action": "next",
            "messages": formatted_messages,
            "parent_message_id": str(uuid.uuid4()),
            "model": "text-davinci-002-render-sha",
            "timezone_offset_min": -480,
            "suggestions": [
                "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
                "I want to cheer up my friend who's having a rough day. Can you suggest a couple short and sweet text messages to go with a kitten gif?",
                "Come up with 5 concepts for a retro-style arcade game.",
                "I have a photoshoot tomorrow. Can you recommend me some colors and outfit options that will look good on camera?"
            ],
            "history_and_training_disabled":False,
            "arkose_token":None,
            "conversation_mode": {
                "kind": "primary_assistant"
            },
            "force_paragen":False,
            "force_rate_limit":False
        }
    else:
        payload = generate_gpts_payload(model, formatted_messages)
        if not payload:
            raise Exception('model is not accessible')
    response = requests.post(url, headers=headers, json=payload, stream=True)
    # print(response)
    return response

def delete_conversation(conversation_id, api_key):
    print(f"[{datetime.now()}] 准备删除的会话id： {conversation_id}")
    if conversation_id:
        patch_url = f"{BASE_URL}/{PROXY_API_PREFIX}/backend-api/conversation/{conversation_id}"
        patch_headers = {
            "Authorization": f"Bearer {api_key}",
        }
        patch_data = {"is_visible": False}
        response = requests.patch(patch_url, headers=patch_headers, json=patch_data)

        if response.status_code == 200:
            print(f"[{datetime.now()}] 删除会话 {conversation_id} 成功")
        else:
            print(f"[{datetime.now()}] PATCH 请求失败: {response.text}")

from PIL import Image
import io
def save_image(image_data, path='images'):
    try:
        # print(f"image_data: {image_data}")
        if not os.path.exists(path):
            os.makedirs(path)
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'image_{current_time}.png'
        full_path = os.path.join(path, filename)
        print(f"完整的文件路径: {full_path}")  # 打印完整路径
        # print(f"filename: {filename}")
        # 使用 PIL 打开图像数据
        with Image.open(io.BytesIO(image_data)) as image:
            # 保存为 PNG 格式
            image.save(os.path.join(path, filename), 'PNG')

        print(f"保存图片成功: {filename}")

        return os.path.join(path, filename)
    except Exception as e:
        print(f"保存图片时出现异常: {e}")



def unicode_to_chinese(unicode_string):
    # 首先将字符串转换为标准的 JSON 格式字符串
    json_formatted_str = json.dumps(unicode_string)
    # 然后将 JSON 格式的字符串解析回正常的字符串
    return json.loads(json_formatted_str)

import re

# 辅助函数：检查是否为合法的引用格式或正在构建中的引用格式
def is_valid_citation_format(text):
    # 完整且合法的引用格式，允许紧跟另一个起始引用标记
    if re.fullmatch(r'\u3010\d+\u2020(source|\u6765\u6e90)\u3011\u3010?', text):
        return True

    # 完整且合法的引用格式
    
    if re.fullmatch(r'\u3010\d+\u2020(source|\u6765\u6e90)\u3011', text):
        return True

    # 合法的部分构建格式
    if re.fullmatch(r'\u3010(\d+)?(\u2020(source|\u6765\u6e90)?)?', text):
        return True

    # 不合法的格式
    return False

# 辅助函数：检查是否为完整的引用格式
# 检查是否为完整的引用格式
def is_complete_citation_format(text):
    return bool(re.fullmatch(r'\u3010\d+\u2020(source|\u6765\u6e90)\u3011\u3010?', text))


# 替换完整的引用格式
def replace_complete_citation(text, citations):
    def replace_match(match):
        citation_number = match.group(1)
        for citation in citations:
            cited_message_idx = citation.get('metadata', {}).get('extra', {}).get('cited_message_idx')
            print(f"cited_message_idx: {cited_message_idx}")
            print(f"citation_number: {citation_number}")
            print(f"is citation_number == cited_message_idx: {cited_message_idx == int(citation_number)}")
            print(f"citation: {citation}")
            if cited_message_idx == int(citation_number):
                url = citation.get("metadata", {}).get("url", "")
                return f"[[{citation_number}]({url})]"
        return match.group(0)  # 如果没有找到对应的引用，返回原文本

    # 使用 finditer 找到第一个匹配项
    match_iter = re.finditer(r'\u3010(\d+)\u2020(source|\u6765\u6e90)\u3011', text)
    first_match = next(match_iter, None)

    if first_match:
        start, end = first_match.span()
        replaced_text = text[:start] + replace_match(first_match) + text[end:]
        remaining_text = text[end:]
    else:
        replaced_text = text
        remaining_text = ""

    is_potential_citation = is_valid_citation_format(remaining_text)

    # 替换掉replaced_text末尾的remaining_text

    print(f"replaced_text: {replaced_text}")
    print(f"remaining_text: {remaining_text}")
    print(f"is_potential_citation: {is_potential_citation}")
    if is_potential_citation:
        replaced_text = replaced_text[:-len(remaining_text)]


    return replaced_text, remaining_text, is_potential_citation

# 定义 Flask 路由
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    print(f"[{datetime.now()}] New Request")
    data = request.json
    messages = data.get('messages')
    model = data.get('model')
    accessible_model_list = get_accessible_model_list()
    if model not in accessible_model_list:
        return jsonify({"error": "model is not accessible"}), 401

    stream = data.get('stream', False)

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401
    api_key = auth_header.split(' ')[1] 
    print(f"api_key: {api_key}")


    upstream_response = send_text_prompt_and_get_response(messages, api_key, stream, model)

    # 在非流式响应的情况下，我们需要一个变量来累积所有的 new_text
    all_new_text = ""

    # 处理流式响应
    def generate():
        nonlocal all_new_text  # 引用外部变量
        chat_message_id = generate_unique_id("chatcmpl")
        # 当前时间戳
        timestamp = int(time.time())

        buffer = ""
        last_full_text = ""  # 用于存储之前所有出现过的 parts 组成的完整文本
        last_full_code = ""
        last_full_code_result = ""
        last_content_type = None  # 用于记录上一个消息的内容类型
        conversation_id = ''
        citation_buffer = ""
        citation_accumulating = False
        for chunk in upstream_response.iter_content(chunk_size=1024):
            if chunk:
                buffer += chunk.decode('utf-8')
                # 检查是否存在 "event: ping"，如果存在，则只保留 "data:" 后面的内容
                if "event: ping" in buffer:
                    if "data:" in buffer:
                        buffer = buffer.split("data:", 1)[1]
                        buffer = "data:" + buffer
                # 使用正则表达式移除特定格式的字符串
                # print("应用正则表达式之前的 buffer:", buffer.replace('\n', '\\n'))
                buffer = re.sub(r'data: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}(\r\n|\r|\n){2}', '', buffer)
                # print("应用正则表达式之后的 buffer:", buffer.replace('\n', '\\n'))



                while 'data:' in buffer and '\n\n' in buffer:
                    end_index = buffer.index('\n\n') + 2
                    complete_data, buffer = buffer[:end_index], buffer[end_index:]
                    # 解析 data 块
                    try:
                        data_json = json.loads(complete_data.replace('data: ', ''))
                        # print(f"data_json: {data_json}")
                        message = data_json.get("message", {})

                        if message == {} or message == None:
                            print(f"message 为空: data_json: {data_json}")

                        message_status = message.get("status")
                        content = message.get("content", {})
                        role = message.get("author", {}).get("role")
                        content_type = content.get("content_type")
                        print(f"content_type: {content_type}")
                        print(f"last_content_type: {last_content_type}")

                        metadata = {}
                        citations = []
                        try:
                            metadata = message.get("metadata", {})
                            citations = metadata.get("citations", [])
                        except:
                            pass
                        name = message.get("author", {}).get("name")
                        if (role == "user" or message_status == "finished_successfully" or role == "system") and role != "tool":
                            # 如果是用户发来的消息，直接舍弃
                            continue
                        try:
                            conversation_id = data_json.get("conversation_id")
                            print(f"conversation_id: {conversation_id}")
                        except:
                            pass
                            # 只获取新的部分
                        new_text = ""
                        is_img_message = False
                        parts = content.get("parts", [])
                        for part in parts:
                            try:
                                # print(f"part: {part}")
                                # print(f"part type: {part.get('content_type')}")
                                if part.get('content_type') == 'image_asset_pointer':
                                    print(f"find img message~")
                                    is_img_message = True
                                    asset_pointer = part.get('asset_pointer').replace('file-service://', '')
                                    print(f"asset_pointer: {asset_pointer}")
                                    image_url = f"{BASE_URL}/{PROXY_API_PREFIX}/backend-api/files/{asset_pointer}/download"

                                    headers = {
                                        "Authorization": f"Bearer {api_key}"
                                    }
                                    image_response = requests.get(image_url, headers=headers)

                                    if image_response.status_code == 200:
                                        download_url = image_response.json().get('download_url')
                                        print(f"download_url: {download_url}")
                                        # 从URL下载图片
                                        # image_data = requests.get(download_url).content
                                        image_download_response = requests.get(download_url)
                                        # print(f"image_download_response: {image_download_response.text}")
                                        if image_download_response.status_code == 200:
                                            print(f"下载图片成功")
                                            image_data = image_download_response.content
                                            today_image_url = save_image(image_data)  # 保存图片，并获取文件名
                                            new_text = f"\n![image]({UPLOAD_BASE_URL}/{today_image_url})\n[下载链接]({UPLOAD_BASE_URL}/{today_image_url})\n"
                                        else:
                                            print(f"下载图片失败: {image_download_response.text}")
                                        if last_content_type == "code":
                                            new_text = "\n```\n" + new_text
                                        print(f"new_text: {new_text}")
                                        is_img_message = True
                                    else:
                                        print(f"获取图片下载链接失败: {image_response.text}")
                            except:
                                pass
                                    

                        if is_img_message == False:
                            # print(f"data_json: {data_json}")
                            if content_type == "multimodal_text" and last_content_type == "code":
                                new_text = "\n```\n" + content.get("text", "")
                            elif role == "tool" and name == "dalle.text2im":
                                print(f"无视消息: {content.get('text', '')}")
                                continue
                            # 代码块特殊处理
                            if content_type == "code" and last_content_type != "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = "\n```\n" + full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = full_code  # 更新完整代码以备下次比较
                                
                            elif last_content_type == "code" and content_type != "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = "\n```\n" + full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = ""  # 更新完整代码以备下次比较

                            elif content_type == "code" and last_content_type == "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = full_code  # 更新完整代码以备下次比较
                                
                            else:
                                # 只获取新的 parts
                                parts = content.get("parts", [])
                                full_text = ''.join(parts)
                                new_text = full_text[len(last_full_text):]
                                last_full_text = full_text  # 更新完整文本以备下次比较
                                if "\u3010" in new_text and not citation_accumulating:
                                    citation_accumulating = True
                                    citation_buffer = citation_buffer + new_text
                                    print(f"开始积累引用: {citation_buffer}")
                                elif citation_accumulating:
                                    citation_buffer += new_text
                                    print(f"积累引用: {citation_buffer}")
                                if citation_accumulating:
                                    if is_valid_citation_format(citation_buffer):
                                        print(f"合法格式: {citation_buffer}")
                                        # 继续积累
                                        if is_complete_citation_format(citation_buffer):

                                            # 替换完整的引用格式
                                            replaced_text, remaining_text, is_potential_citation = replace_complete_citation(citation_buffer, citations)
                                            # print(replaced_text)  # 输出替换后的文本
                                            new_text = replaced_text
                                            
                                            if(is_potential_citation):
                                                citation_buffer = remaining_text
                                            else:
                                                citation_accumulating = False
                                                citation_buffer = ""
                                            print(f"替换完整的引用格式: {new_text}")
                                        else:
                                            continue
                                    else:
                                        # 不是合法格式，放弃积累并响应
                                        print(f"不合法格式: {citation_buffer}")
                                        new_text = citation_buffer
                                        citation_accumulating = False
                                        citation_buffer = ""


                            # Python 工具执行输出特殊处理
                            if role == "tool" and name == "python" and last_content_type != "execution_output" and content_type != None:
                                

                                full_code_result = ''.join(content.get("text", ""))
                                new_text = "`Result:` \n```\n" + full_code_result[len(last_full_code_result):]
                                if last_content_type == "code":
                                    new_text = "\n```\n" + new_text
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = full_code_result  # 更新完整代码以备下次比较
                            elif last_content_type == "execution_output" and (role != "tool" or name != "python") and content_type != None:
                                # new_text = content.get("text", "") + "\n```"
                                full_code_result = ''.join(content.get("text", ""))
                                new_text = full_code_result[len(last_full_code_result):] + "\n```\n"
                                if content_type == "code":
                                    new_text =  new_text + "\n```\n"
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = ""  # 更新完整代码以备下次比较
                            elif last_content_type == "execution_output" and role == "tool" and name == "python" and content_type != None:
                                full_code_result = ''.join(content.get("text", ""))
                                new_text = full_code_result[len(last_full_code_result):]
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = full_code_result

                        # print(f"[{datetime.now()}] 收到数据: {data_json}")
                        # print(f"[{datetime.now()}] 收到的完整文本: {full_text}")
                        # print(f"[{datetime.now()}] 上次收到的完整文本: {last_full_text}")
                        # print(f"[{datetime.now()}] 新的文本: {new_text}")

                        # 更新 last_content_type
                        if content_type != None:
                            last_content_type = content_type if role != "user" else last_content_type

                        
                        new_data = {
                            "id": chat_message_id,
                            "object": "chat.completion.chunk",
                            "created": timestamp,
                            "model": message.get("metadata", {}).get("model_slug"),
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {
                                        "content": ''.join(new_text)
                                    },
                                    "finish_reason": None
                                }
                            ]
                        }
                        # print(f"Role: {role}")
                        print(f"[{datetime.now()}] 发送消息: {new_text}")
                        tmp = 'data: ' + json.dumps(new_data, ensure_ascii=False) + '\n\n'
                        # print(f"[{datetime.now()}] 发送数据: {tmp}")
                        # 累积 new_text
                        all_new_text += new_text
                        yield 'data: ' + json.dumps(new_data, ensure_ascii=False) + '\n\n'
                    except json.JSONDecodeError:
                        # print("JSON 解析错误")
                        print(f"[{datetime.now()}] 发送数据: {complete_data}")
                        if complete_data == 'data: [DONE]\n\n':
                            print(f"[{datetime.now()}] 会话结束")
                            yield complete_data
        if citation_buffer != "":
            new_data = {
                "id": chat_message_id,
                "object": "chat.completion.chunk",
                "created": timestamp,
                "model": message.get("metadata", {}).get("model_slug"),
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": ''.join(citation_buffer)
                        },
                        "finish_reason": None
                    }
                ]
            }
            tmp = 'data: ' + json.dumps(new_data) + '\n\n'
            # print(f"[{datetime.now()}] 发送数据: {tmp}")
            # 累积 new_text
            all_new_text += citation_buffer
            yield 'data: ' + json.dumps(new_data) + '\n\n'
        if buffer:
            # print(f"[{datetime.now()}] 最后的数据: {buffer}")
            delete_conversation(conversation_id, api_key)
            try:
                buffer_json = json.loads(buffer)
                error_message = buffer_json.get("detail", {}).get("message", "未知错误")
                error_data = {
                            "id": chat_message_id,
                            "object": "chat.completion.chunk",
                            "created": timestamp,
                            "model": "error",
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {
                                        "content": ''.join("```\n" + error_message + "\n```")
                                    },
                                    "finish_reason": None
                                }
                            ]
                        }
                tmp = 'data: ' + json.dumps(error_data) + '\n\n'
                print(f"[{datetime.now()}] 发送最后的数据: {tmp}")
                # 累积 new_text
                all_new_text += ''.join("```\n" + error_message + "\n```")
                yield 'data: ' + json.dumps(error_data) + '\n\n'
            except:
                # print("JSON 解析错误")
                print(f"[{datetime.now()}] 发送最后的数据: {buffer}")
                yield buffer

        delete_conversation(conversation_id, api_key)   
            

    if not stream:
        # 执行流式响应的生成函数来累积 all_new_text
        # 迭代生成器对象以执行其内部逻辑
        for _ in generate():
            pass
        # 构造响应的 JSON 结构
        response_json = {
            "id": generate_unique_id("chatcmpl"),
            "object": "chat.completion",
            "created": int(time.time()),  # 使用当前时间戳
            "model": model,  # 使用请求中指定的模型
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": all_new_text  # 使用累积的文本
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                # 这里的 token 计数需要根据实际情况计算
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            "system_fingerprint": None
        }

        # 返回 JSON 响应
        return jsonify(response_json)
    else:            
        return Response(generate(), mimetype='text/event-stream')


@app.route('/v1/images/generations', methods=['POST'])
def images_generations():
    print(f"[{datetime.now()}] New Img Request")
    data = request.json
    # messages = data.get('messages')
    model = data.get('model')
    accessible_model_list = get_accessible_model_list()
    if model not in accessible_model_list:
        return jsonify({"error": "model is not accessible"}), 401
    
    prompt = data.get('prompt', '')

    # stream = data.get('stream', False)

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header is missing or invalid"}), 401
    api_key = auth_header.split(' ')[1] 
    print(f"api_key: {api_key}")

    image_urls = []

    messages = [
        {
            "role": "user",
            "content": prompt,
            "hasName": False
        }
    ]

    upstream_response = send_text_prompt_and_get_response(messages, api_key, False, model)

    # 在非流式响应的情况下，我们需要一个变量来累积所有的 new_text
    all_new_text = ""

    # 处理流式响应
    def generate():
        nonlocal all_new_text  # 引用外部变量
        chat_message_id = generate_unique_id("chatcmpl")
        # 当前时间戳
        timestamp = int(time.time())

        buffer = ""
        last_full_text = ""  # 用于存储之前所有出现过的 parts 组成的完整文本
        last_full_code = ""
        last_full_code_result = ""
        last_content_type = None  # 用于记录上一个消息的内容类型
        conversation_id = ''
        citation_buffer = ""
        citation_accumulating = False
        for chunk in upstream_response.iter_content(chunk_size=1024):
            if chunk:
                buffer += chunk.decode('utf-8')
                # 检查是否存在 "event: ping"，如果存在，则只保留 "data:" 后面的内容
                if "event: ping" in buffer:
                    if "data:" in buffer:
                        buffer = buffer.split("data:", 1)[1]
                        buffer = "data:" + buffer
                # 使用正则表达式移除特定格式的字符串
                # print("应用正则表达式之前的 buffer:", buffer.replace('\n', '\\n'))
                buffer = re.sub(r'data: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}(\r\n|\r|\n){2}', '', buffer)
                # print("应用正则表达式之后的 buffer:", buffer.replace('\n', '\\n'))



                while 'data:' in buffer and '\n\n' in buffer:
                    end_index = buffer.index('\n\n') + 2
                    complete_data, buffer = buffer[:end_index], buffer[end_index:]
                    # 解析 data 块
                    try:
                        data_json = json.loads(complete_data.replace('data: ', ''))
                        # print(f"data_json: {data_json}")
                        message = data_json.get("message", {})

                        if message == {} or message == None:
                            print(f"message 为空: data_json: {data_json}")

                        message_status = message.get("status")
                        content = message.get("content", {})
                        role = message.get("author", {}).get("role")
                        content_type = content.get("content_type")
                        print(f"content_type: {content_type}")
                        print(f"last_content_type: {last_content_type}")

                        metadata = {}
                        citations = []
                        try:
                            metadata = message.get("metadata", {})
                            citations = metadata.get("citations", [])
                        except:
                            pass
                        name = message.get("author", {}).get("name")
                        if (role == "user" or message_status == "finished_successfully" or role == "system") and role != "tool":
                            # 如果是用户发来的消息，直接舍弃
                            continue
                        try:
                            conversation_id = data_json.get("conversation_id")
                            print(f"conversation_id: {conversation_id}")
                        except:
                            pass
                            # 只获取新的部分
                        new_text = ""
                        is_img_message = False
                        parts = content.get("parts", [])
                        for part in parts:
                            try:
                                # print(f"part: {part}")
                                # print(f"part type: {part.get('content_type')}")
                                if part.get('content_type') == 'image_asset_pointer':
                                    print(f"find img message~")
                                    is_img_message = True
                                    asset_pointer = part.get('asset_pointer').replace('file-service://', '')
                                    print(f"asset_pointer: {asset_pointer}")
                                    image_url = f"{BASE_URL}/{PROXY_API_PREFIX}/backend-api/files/{asset_pointer}/download"

                                    headers = {
                                        "Authorization": f"Bearer {api_key}"
                                    }
                                    image_response = requests.get(image_url, headers=headers)

                                    if image_response.status_code == 200:
                                        download_url = image_response.json().get('download_url')
                                        print(f"download_url: {download_url}")
                                        # 从URL下载图片
                                        # image_data = requests.get(download_url).content
                                        image_download_response = requests.get(download_url)
                                        # print(f"image_download_response: {image_download_response.text}")
                                        if image_download_response.status_code == 200:
                                            print(f"下载图片成功")
                                            image_data = image_download_response.content
                                            today_image_url = save_image(image_data)  # 保存图片，并获取文件名
                                            # new_text = f"\n![image]({UPLOAD_BASE_URL}/{today_image_url})\n[下载链接]({UPLOAD_BASE_URL}/{today_image_url})\n"
                                            image_link = f"{UPLOAD_BASE_URL}/{today_image_url}"
                                            image_urls.append(image_link)  # 将图片链接保存到列表中
                                            new_text = ""
                                        else:
                                            print(f"下载图片失败: {image_download_response.text}")
                                        if last_content_type == "code":
                                            new_text = new_text
                                            # new_text = "\n```\n" + new_text
                                        print(f"new_text: {new_text}")
                                        is_img_message = True
                                    else:
                                        print(f"获取图片下载链接失败: {image_response.text}")
                            except:
                                pass
                                    

                        if is_img_message == False:
                            # print(f"data_json: {data_json}")
                            if content_type == "multimodal_text" and last_content_type == "code":
                                new_text = "\n```\n" + content.get("text", "")
                            elif role == "tool" and name == "dalle.text2im":
                                print(f"无视消息: {content.get('text', '')}")
                                continue
                            # 代码块特殊处理
                            if content_type == "code" and last_content_type != "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = "\n```\n" + full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = full_code  # 更新完整代码以备下次比较
                                
                            elif last_content_type == "code" and content_type != "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = "\n```\n" + full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = ""  # 更新完整代码以备下次比较

                            elif content_type == "code" and last_content_type == "code" and content_type != None:
                                full_code = ''.join(content.get("text", ""))
                                new_text = full_code[len(last_full_code):]
                                # print(f"full_code: {full_code}")
                                # print(f"last_full_code: {last_full_code}")
                                # print(f"new_text: {new_text}")
                                last_full_code = full_code  # 更新完整代码以备下次比较
                                
                            else:
                                # 只获取新的 parts
                                parts = content.get("parts", [])
                                full_text = ''.join(parts)
                                new_text = full_text[len(last_full_text):]
                                last_full_text = full_text  # 更新完整文本以备下次比较
                                if "\u3010" in new_text and not citation_accumulating:
                                    citation_accumulating = True
                                    citation_buffer = citation_buffer + new_text
                                    print(f"开始积累引用: {citation_buffer}")
                                elif citation_accumulating:
                                    citation_buffer += new_text
                                    print(f"积累引用: {citation_buffer}")
                                if citation_accumulating:
                                    if is_valid_citation_format(citation_buffer):
                                        print(f"合法格式: {citation_buffer}")
                                        # 继续积累
                                        if is_complete_citation_format(citation_buffer):

                                            # 替换完整的引用格式
                                            replaced_text, remaining_text, is_potential_citation = replace_complete_citation(citation_buffer, citations)
                                            # print(replaced_text)  # 输出替换后的文本
                                            new_text = replaced_text
                                            
                                            if(is_potential_citation):
                                                citation_buffer = remaining_text
                                            else:
                                                citation_accumulating = False
                                                citation_buffer = ""
                                            print(f"替换完整的引用格式: {new_text}")
                                        else:
                                            continue
                                    else:
                                        # 不是合法格式，放弃积累并响应
                                        print(f"不合法格式: {citation_buffer}")
                                        new_text = citation_buffer
                                        citation_accumulating = False
                                        citation_buffer = ""


                            # Python 工具执行输出特殊处理
                            if role == "tool" and name == "python" and last_content_type != "execution_output" and content_type != None:
                                

                                full_code_result = ''.join(content.get("text", ""))
                                new_text = "`Result:` \n```\n" + full_code_result[len(last_full_code_result):]
                                if last_content_type == "code":
                                    new_text = "\n```\n" + new_text
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = full_code_result  # 更新完整代码以备下次比较
                            elif last_content_type == "execution_output" and (role != "tool" or name != "python") and content_type != None:
                                # new_text = content.get("text", "") + "\n```"
                                full_code_result = ''.join(content.get("text", ""))
                                new_text = full_code_result[len(last_full_code_result):] + "\n```\n"
                                if content_type == "code":
                                    new_text =  new_text + "\n```\n"
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = ""  # 更新完整代码以备下次比较
                            elif last_content_type == "execution_output" and role == "tool" and name == "python" and content_type != None:
                                full_code_result = ''.join(content.get("text", ""))
                                new_text = full_code_result[len(last_full_code_result):]
                                # print(f"full_code_result: {full_code_result}")
                                # print(f"last_full_code_result: {last_full_code_result}")
                                # print(f"new_text: {new_text}")
                                last_full_code_result = full_code_result

                        # print(f"[{datetime.now()}] 收到数据: {data_json}")
                        # print(f"[{datetime.now()}] 收到的完整文本: {full_text}")
                        # print(f"[{datetime.now()}] 上次收到的完整文本: {last_full_text}")
                        # print(f"[{datetime.now()}] 新的文本: {new_text}")

                        # 更新 last_content_type
                        if content_type != None:
                            last_content_type = content_type if role != "user" else last_content_type

                        
                        new_data = {
                            "id": chat_message_id,
                            "object": "chat.completion.chunk",
                            "created": timestamp,
                            "model": message.get("metadata", {}).get("model_slug"),
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {
                                        "content": ''.join(new_text)
                                    },
                                    "finish_reason": None
                                }
                            ]
                        }
                        # print(f"Role: {role}")
                        print(f"[{datetime.now()}] 发送消息: {new_text}")
                        tmp = 'data: ' + json.dumps(new_data, ensure_ascii=False) + '\n\n'
                        # print(f"[{datetime.now()}] 发送数据: {tmp}")
                        # 累积 new_text
                        all_new_text += new_text
                        yield 'data: ' + json.dumps(new_data, ensure_ascii=False) + '\n\n'
                    except json.JSONDecodeError:
                        # print("JSON 解析错误")
                        print(f"[{datetime.now()}] 发送数据: {complete_data}")
                        if complete_data == 'data: [DONE]\n\n':
                            print(f"[{datetime.now()}] 会话结束")
                            yield complete_data
        if citation_buffer != "":
            new_data = {
                "id": chat_message_id,
                "object": "chat.completion.chunk",
                "created": timestamp,
                "model": message.get("metadata", {}).get("model_slug"),
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": ''.join(citation_buffer)
                        },
                        "finish_reason": None
                    }
                ]
            }
            tmp = 'data: ' + json.dumps(new_data) + '\n\n'
            # print(f"[{datetime.now()}] 发送数据: {tmp}")
            # 累积 new_text
            all_new_text += citation_buffer
            yield 'data: ' + json.dumps(new_data) + '\n\n'
        if buffer:
            # print(f"[{datetime.now()}] 最后的数据: {buffer}")
            delete_conversation(conversation_id, api_key)
            try:
                buffer_json = json.loads(buffer)
                error_message = buffer_json.get("detail", {}).get("message", "未知错误")
                error_data = {
                            "id": chat_message_id,
                            "object": "chat.completion.chunk",
                            "created": timestamp,
                            "model": "error",
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {
                                        "content": ''.join("```\n" + error_message + "\n```")
                                    },
                                    "finish_reason": None
                                }
                            ]
                        }
                tmp = 'data: ' + json.dumps(error_data) + '\n\n'
                print(f"[{datetime.now()}] 发送最后的数据: {tmp}")
                # 累积 new_text
                all_new_text += ''.join("```\n" + error_message + "\n```")
                yield 'data: ' + json.dumps(error_data) + '\n\n'
            except:
                # print("JSON 解析错误")
                print(f"[{datetime.now()}] 发送最后的数据: {buffer}")
                yield buffer

        delete_conversation(conversation_id, api_key)   
            
    # 执行流式响应的生成函数来累积 all_new_text
    # 迭代生成器对象以执行其内部逻辑
    for _ in generate():
        pass
    # 构造响应的 JSON 结构
    response_json = {
        "created": int(time.time()),  # 使用当前时间戳
        "reply": all_new_text,  # 使用累积的文本
        "data": [{"url": url} for url in image_urls]  # 将图片链接列表转换为所需格式
    }

    # 返回 JSON 响应
    return jsonify(response_json)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# 特殊的 OPTIONS 请求处理器
@app.route('/v1/chat/completions', methods=['OPTIONS'])
def options_handler():
    print(f"[{datetime.now()}] Options Request")
    return Response(status=200)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"[{datetime.now()}] 未知请求: {path}")
    print(f"[{datetime.now()}] 请求方法: {request.method}")
    print(f"[{datetime.now()}] 请求头: {request.headers}")
    print(f"[{datetime.now()}] 请求体: {request.data}")

    return jsonify({"message": "Unknown"}), 200


@app.route('/images/<filename>')
@cross_origin()  # 使用装饰器来允许跨域请求
def get_image(filename):
    # 检查文件是否存在
    if not os.path.isfile(os.path.join('images', filename)):
        return "文件不存在哦！", 404
    return send_from_directory('images', filename)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0')

