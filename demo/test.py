import websocket
import json
import time
import threading

WS_URL = "ws://101.34.75.156:8090/websocket/chat/920/1ifogtef/websocket"
NICKNAME = "PythonSockJSBot"

def send_sockjs(ws, obj):
    """SockJS 发送封装，消息必须是 a[...] 格式"""
    data = json.dumps(obj, ensure_ascii=False)
    sockjs_msg = json.dumps([data])
    ws.send(sockjs_msg)

def on_open(ws):
    print("✅ 已连接 SockJS")

    # # 发送 JOIN 消息
    # join_msg = {
    #     "type": "JOIN",
    #     "senderNickname": NICKNAME,
    #     "content": "",
    #     "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    # }
    # send_sockjs(ws, join_msg)
    # print("➡️ 已发送 JOIN 消息")

    # 启动输入线程
    def input_loop():
        while True:
            try:
                content = input("\n请输入要发送的消息内容 (输入 'exit' 退出): ")
                if content.lower() == "exit":
                    print("👋 已退出输入循环")
                    ws.close()
                    break

                count_str = input("请输入要发送的条数: ")
                try:
                    count = int(count_str)
                except ValueError:
                    print("⚠️ 条数必须是数字，已默认 1 条")
                    count = 1

                for i in range(count):
                    text_msg = {
                        "type": "TEXT",
                        "senderNickname": NICKNAME,
                        "content": f"{content} ({i+1}/{count})",
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                    }
                    send_sockjs(ws, text_msg)
                    print(f"➡️ 已发送: {text_msg['content']}")
                    time.sleep(0.3)  # 适当延时，避免刷太快
            except (EOFError, KeyboardInterrupt):
                print("\n👋 输入中断，关闭连接")
                ws.close()
                break

    threading.Thread(target=input_loop, daemon=True).start()

def on_message(ws, message):
    if message == "o":
        print("📡 SockJS: 连接打开")
    elif message == "h":
        print("💓 SockJS: 心跳")
    elif message.startswith("a["):
        try:
            data_list = json.loads(message[1:])
            for item in data_list:
                obj = json.loads(item)
                print("📩 收到:", obj)
        except Exception as e:
            print("⚠️ 解析失败:", message, e)
    else:
        print("📩 原始消息:", message)

def on_close(ws, code, reason):
    print("❌ 连接关闭", code, reason)

def on_error(ws, error):
    print("⚠️ 出错:", error)

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )
    ws.run_forever()
