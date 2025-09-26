import requests
import json
from datetime import datetime

def send_alert_to_feishu(title, test_url, case_id, project_name, webhook_url):
    # 构建卡片消息内容
    card_elements = []

    card_elements.append({
        "tag": "div",
        "fields": [
            {
                "is_short": True,
                "text": {
                    "content": f"**Project_name:**\n{project_name}",
                    "tag": "lark_md"
                }
            },
                {
                "is_short": True,
                "text": {
                    "content": f"**Case id:**\n{case_id}",
                    "tag": "lark_md"
                }
            },
            {
                "is_short": True,
                "text": {
                    "content": f"**Replay Report Link:**\n[Report]({test_url})",
                    "tag": "lark_md"
                }
            },
        ]
    })

    # 添加分隔线
    card_elements.append({"tag": "hr"})

    # card_elements.append({
    #     "tag": "div",
    #     "fields": [
    #         {
    #             "is_short": True,
    #             "text": {
    #                 "content": f"**metric_name :**\n{metric_name_str}",
    #                 "tag": "lark_md"
    #             }
    #         },
    #             {
    #             "is_short": True,
    #             "text": {
    #                 "content": f"<at id={user_id}></at>",
    #                 "tag": "lark_md"
    #             },
    #         }
    #     ]
    # })

    # 添加分隔线
    card_elements.append({"tag": "hr"})

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

# send_alert_to_feishu("oom", test_url, uuid, project_name, webhook_url, metric_name_ssh_list, user_id)