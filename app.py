from flask import Flask, request, jsonify
import requests  # 用於發送HTTP請求
from flask_cors import CORS
import os
import openai
from openai import OpenAI
client=OpenAI()
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)  # 啟用 CORS

@app.route("/get_weather", methods=["POST"])
def get_weather():
    # 從前端的請求中獲取經緯度參數p
    location = request.json  # {"lat": 48.8566, "lon": 2.3522}
    latitude = location.get("lat")
    longitude = location.get("lon")

    # 替換為您的天氣 API URL 和密鑰
    WEATHER_API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    response = requests.get(WEATHER_API_URL) #是使用 Python 的 requests 庫向 API 發送一個 HTTP GET 請求，來獲取網路上的數據。
    if response.status_code == 200:
        data = response.json() #將 JSON 格式的字串自動轉換成 Python 的字典
        current = data['current'] #從字典中提取了當前的天氣信息
        suggestion=get_completion(current)
        # 返回天氣數據和建議
        return jsonify({"weather": current, "suggestion": suggestion})
    else:
        return '{"error": "无法获取天气数据"}',500
    


# 定義 get_completion 函數，用於生成基於天氣的建議
def get_completion(current, model="gpt-3.5-turbo"):
    prompt = f"""你是一位天氣助手。以下是當前的天氣數據：
    溫度：{current.get("temperature_2m", "未知")}
    風速：{current.get("wind_speed_10m", "未知")}
    根據這些天氣資訊，請提供一些建議。"""

    # 調用 OpenAI API 生成建議
    response =client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位天氣助手，根據當前天氣提供建議。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    # 返回生成的建議文字
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)