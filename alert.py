import requests
import json
from datetime import datetime

def send_alert_to_feishu(webhook_url, title, data):
    # 构建卡片消息内容
    card_elements = []
    for name, value in data.items():
        if "http" in value:
            card_elements.append({
            "tag": "div",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "content": f"**{name} :**\n[Report]({value})",
                        "tag": "lark_md"
                    }
                }
            ]
            })
       
        else:    
            card_elements.append({
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**{name} :**\n{value}",
                            "tag": "lark_md"
                        }
                    }
                ]
            })

   # 构建整个消息
    message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "content": f"🚨 {title} 状态告警",
                    "tag": "plain_text"
                },
                "template": "red"
            },
            "elements": card_elements
        }
    }

    # 发送 POST 请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 检查响应
    if response.status_code == 200:
        print("告警信息发送成功！")
    else:
        print(f"告警信息发送失败，状态码：{response.status_code}")
        print(f"响应内容：{response.text}") 

# title = "TEST"
# data = {
#     "project_name": "NT2",
#     "case_id": "20240525T144500_LJ1EFAUU1NG000025",
#     "test_url": "https://aip.nioint.com/#/adsim/hilReplay/management/details?exec_plan_id=",
# }

# send_alert_to_feishu("https://open.feishu.cn/open-apis/bot/v2/hook/63871227-dec7-401c-bd48-23e03b82baaa", "TEST", data)