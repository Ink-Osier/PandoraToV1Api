from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# 确保 images 文件夹存在
os.makedirs('images', exist_ok=True)

@app.route('/images/<filename>')
def get_image(filename):
    # 检查文件是否存在
    if not os.path.isfile(os.path.join('images', filename)):
        return "文件不存在哦！", 404
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23333)
