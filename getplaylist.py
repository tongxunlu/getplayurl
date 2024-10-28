import json
import time
import requests
import os

uid = os.getenv('UID')
json_file = 'playlist'

channel_map = json.loads( os.getenv('ROOTIDS') )
print("channel_map类型是:"+type(channel_map))  # 检查类型
print("channel_map内容是:"+channel_map)        # 检查内容
root_ids = {}


def get_channel_url(channel_id):
    # 分割 ID 以处理可能的后缀
    temp_id = channel_id.split("-")
    base_id = temp_id[0] 
    temp_index = 1 if len(temp_id) > 1 else 0  # 根据后缀的存在确定索引

    # 请求的 URL 和数据
    url = os.getenv('LIVE_API')
    post_data = {
        "rate": "",
        "systemType": "android",
        "model": "Sony-BRAVIA 4K",
        "id": base_id,
        "userId": "",
        "clientSign": "cctvVideo",
        "deviceId": {
            "serial": "",
            "imei": "",
            "android_id": ""
        }
    }

    headers = json.loads( os.getenv('HEADERS') )

    # 发送 POST 请求
    response = requests.post(url, json=post_data, headers=headers)

    # 解析 JSON 响应
    if response.status_code == 200:
        obj = response.json()

        # 检查响应中是否包含 URL
        video_list = obj.get('data', {}).get('videoList', [])
        if video_list:  # 如果 videoList 不为空
            return video_list[temp_index]['url']  # 返回对应索引的播放 URL

    return "bad req"  # 如果未找到 URL，返回错误消息


# Clear the JSON file
with open(json_file, 'w') as f:
    f.write("")

# 合并为一个字典
merged_channel_map = {}
for channel in channel_map:
    merged_channel_map.update(channel)
    
# Fetch channel URLs
for channel, live_id in channel_map.items():
    root_id = get_channel_url(live_id)
    root_ids[channel] = root_id
    time.sleep(0.5)  # Set request interval (0.5 seconds)

# Write the JSON data to file
with open(json_file, 'w') as f:
    json.dump(root_ids, f)

# Print the JSON data
print(json.dumps(root_ids))
