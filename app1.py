from flask import Flask, request, jsonify
import requests  # 用於發送HTTP請求


app = Flask(__name__)

# 替換為您的天氣 API URL 和密鑰
WEATHER_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization=CWA-12F778E5-D990-4619-BAB7-893431375F78&format=JSON"

@app.route("/get_weather", methods=["POST"])
def get_weather():
    # 從前端的請求中獲取地點參數
    location = request.json.get("location", "")
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization=CWA-12F778E5-D990-4619-BAB7-893431375F78&format=JSON"
    response = requests.get(url)  # 發送請求獲取數據
    if response.status_code == 200:
        data = response.json()
        # 初始化空字符串用於存儲結果
        result = []

        # 遍歷每個記錄
        for record in data['records']['record']:
            dataset_description = record['datasetInfo']['datasetDescription']  # 提取 datasetDescription
            content_text = record['contents']['content']['contentText'].strip()  # 提取內容文本
            hazards = record['hazardConditions']['hazards']['hazard']

            # 構建每個位置的天氣信息
            weather_info = f"{dataset_description}: {content_text}\n"

            # 提取和顯示每個 hazard 的位置
            for hazard in hazards:
                phenomena = hazard['info']['phenomena']  # 提取現象
                significance = hazard['info']['significance']  # 提取重要性
                affected_locations = hazard['info']['affectedAreas']['location']

                # 格式化位置信息
                locations = [loc['locationName'] for loc in affected_locations]
                weather_info += f"现象: {phenomena}, 重要性: {significance}, 受影响地区: {', '.join(locations)}\n"

            result.append(weather_info)

        return '\n'.join(result)  # 返回所有天氣信息的字符串
    else:
        return '{"error": "无法获取天气数据"}'

if __name__ == "__main__":
    app.run(debug=True)
