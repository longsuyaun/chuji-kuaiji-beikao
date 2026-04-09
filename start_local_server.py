#!/usr/bin/env python3
"""
初级会计备考 - 本地局域网服务器
支持多设备访问，自动获取局域网 IP
"""

import http.server
import socketserver
import os
import sys
import socket
from datetime import datetime

# 配置
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    """获取局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_all_ips():
    """获取所有可用的 IP 地址"""
    hostname = socket.gethostname()
    ips = []
    
    # 局域网 IP
    local_ip = get_local_ip()
    ips.append(f"http://{local_ip}:{PORT}")
    
    # localhost
    ips.append(f"http://localhost:{PORT}")
    ips.append(f"http://127.0.0.1:{PORT}")
    
    # 主机名
    try:
        host_ip = socket.gethostbyname(hostname)
        if host_ip != local_ip:
            ips.append(f"http://{host_ip}:{PORT}")
    except:
        pass
    
    return ips

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {args[0]}")

def print_welcome():
    """打印欢迎信息"""
    print("=" * 60)
    print("📚 初级会计备考 - 本地局域网服务器")
    print("=" * 60)
    print()
    print(f"📂 服务目录：{DIRECTORY}")
    print(f"🔌 端口：{PORT}")
    print()
    print("📱 访问地址：")
    for ip in get_all_ips():
        print(f"   🌐 {ip}")
    print()
    print("💡 使用说明：")
    print("   - 电脑访问：使用 localhost 或局域网 IP")
    print("   - 手机/平板访问：使用局域网 IP")
    print("   - 确保设备在同一 WiFi 网络下")
    print()
    print("🛑 停止服务：Ctrl + C")
    print()
    print("=" * 60)
    print("🚀 服务器启动中...")
    print("=" * 60)

def main():
    """主函数"""
    # 切换到项目目录
    os.chdir(DIRECTORY)
    
    # 打印欢迎信息
    print_welcome()
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            print(f"\n✅ 服务器已启动！")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 正在停止服务器...")
            httpd.shutdown()
            print("✅ 服务器已停止")
            sys.exit(0)

if __name__ == "__main__":
    main()
