from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("收到 GitHub Webhook 请求，开始执行部署脚本...")
    try:
        subprocess.run(["/bin/bash", "deploy.sh"], check=True)
        return "OK", 200
    except subprocess.CalledProcessError as e:
        print("部署失败：", e)
        return "Error", 500

if __name__ == "__main__":
    # 监听所有 IP 的 9000 端口
    app.run(host="0.0.0.0", port=9000)