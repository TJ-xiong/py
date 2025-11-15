#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青龙面板Clash配置接收接口
只有一个POST接口，接收clash和token参数，校验后保存配置
运行1分钟后自动关闭
"""

from flask import Flask, request, jsonify
import os
import threading
import time
import socket

app = Flask(__name__)

# 配置保存目录
CONFIG_DIR = "/ql/static/dist/clash"
os.makedirs(CONFIG_DIR, exist_ok=True)

# 有效token列表
VALID_TOKENS = ["qinglong_token_2024"]


def get_host_info():
    """获取主机网络信息"""
    try:
        # 获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        # 获取主机名
        hostname = socket.gethostname()

        return local_ip, hostname
    except Exception as e:
        print(f"⚠️ 获取网络信息失败: {e}")
        return "未知", "未知"


def auto_shutdown_timer(minutes=1):
    """自动关闭计时器"""

    def shutdown():
        seconds = minutes * 60
        print(f"⏰ 服务器将在 {minutes} 分钟({seconds}秒)后自动关闭...")
        time.sleep(seconds)
        print("🛑 自动关闭服务器")
        # 强制退出
        os._exit(0)

    timer_thread = threading.Thread(target=shutdown)
    timer_thread.daemon = True
    timer_thread.start()


@app.route('/api/clash/upload', methods=['POST'])
def upload_clash_config():
    """
    上传Clash配置接口
    POST参数:
    - clash: Clash配置文件内容
    - token: 访问令牌
    """
    try:
        # 获取参数
        data = request.get_json() if request.is_json else request.form

        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据为空'
            }), 400

        clash_config = data.get('clash', '').strip()
        token = data.get('token', '').strip()

        # 校验参数
        if not clash_config:
            return jsonify({
                'success': False,
                'message': 'clash参数不能为空'
            }), 400

        if not token:
            return jsonify({
                'success': False,
                'message': 'token参数不能为空'
            }), 400

        # 校验token
        if token not in VALID_TOKENS:
            return jsonify({
                'success': False,
                'message': 'token无效'
            }), 401

        # 保存配置
        filename = "XFLTD.yaml"
        filepath = os.path.join(CONFIG_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clash_config)

        print(f"✅ 配置已保存: {filename}")
        print(f"📁 保存路径: {filepath}")
        print(f"📊 文件大小: {len(clash_config)} 字符")

        return jsonify({
            'success': True,
            'message': '配置保存成功',
            'filename': filename,
            'filepath': filepath,
            'size': len(clash_config)
        })

    except Exception as e:
        print(f"❌ 处理请求出错: {e}")
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'success': True,
        'message': '服务运行正常',
        'timestamp': time.time()
    })


def run_server():
    """运行服务器"""
    # 获取网络信息
    local_ip, hostname = get_host_info()
    port = 5000

    print("=" * 60)
    print("🚀 Clash配置接收服务启动成功")
    print("=" * 60)
    print(f"🏷️  主机名: {hostname}")
    print(f"📍 本机IP: {local_ip}")
    print(f"🔧 服务端口: {port}")
    print(f"📡 内部访问: http://localhost:{port}/api/clash/upload")
    print(f"🌐 外部访问: http://{local_ip}:{port}/api/clash/upload")
    print(f"❤️  健康检查: http://{local_ip}:{port}/api/health")
    print(f"💾 配置目录: {CONFIG_DIR}")
    print(f"📄 目标文件: XFLTD.yaml")
    print(f"🔑 有效Token: {VALID_TOKENS}")
    print(f"⏰ 自动关闭: 1分钟后")
    print("=" * 60)
    print("📝 使用示例:")
    print(f'curl -X POST http://{local_ip}:5000/api/clash/upload \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"clash": "你的配置内容", "token": "qinglong_token_2024"}\'')
    print("=" * 60)

    # 启动自动关闭计时器
    auto_shutdown_timer(minutes=1)

    # 运行Flask服务器
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


if __name__ == '__main__':
    run_server()