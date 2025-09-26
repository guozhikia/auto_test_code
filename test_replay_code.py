import requests
import re
import time
import json
from datetime import datetime

from config import env_info, feishu_webhook_url
from alert import send_alert_to_feishu




class TestCode():
    def __init__(self):
        self.env_info = env_info
        self.headers = {
            'Content-Type': 'application/json',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDksImlzcyI6ImhpbHJlcGxheSIsImV4cCI6MTc3NTA0MjQ3N30.20D_y0mAHmAB2MqOcBq-kQbNk8rKDgMfJKzN67jHU_o'
        }
        self.check_result = {"NT2": {"update_queue":"", "put_code":"", "bundle_valid":"", "send_test_task": "", "task_create_status": "", "task_exec_status": "", "select_task_exec_status": False, "check_test_result": "", "put_all_code": []},
                            "NT3_ALPS": {"update_queue":"", "put_code":"", "bundle_valid":"", "send_test_task": "", "task_create_status": "", "task_exec_status": "", "select_task_exec_status": False, "check_test_result": "", "put_all_code": []},
                            "NT3_LEO": {"update_queue":"", "put_code":"", "bundle_valid":"", "send_test_task": "", "task_create_status": "", "task_exec_status": "", "select_task_exec_status": False, "check_test_result": "", "put_all_code": []},
                            "NT25": {},
                            }
    def update_queue(self):
        for platform, info in self.env_info.items():
            if platform == "NT25":
                continue
            url = f"https://hilreplay.nioint.com/api/bench/queue/update?queueName={info['test_queue_name']}"
            
            data = [
                    {   
                        "ID": info['host_id'],
                        "Name": info['host_ip'],
                        "Hostname": info["hostname"],
                        "Resourcepool": "hil",
                        "QueueName": info['test_queue_name'],
                    }
                ]
            
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=300)
            print(response.text)
            if response.status_code == 200 and json.loads(response.text).get('success'):
                print(f"{platform}: Update queue {info['test_queue_name']} success")
                self.check_result[platform]["update_queue"] = True
            else:
                self.check_result[platform]["update_queue"] = False
                raise Exception(f"{platform}: Update queue {info['test_queue_name']} failed, status code: {response.status_code}")


    def put_code(self):
        for platform, info in self.env_info.items():
            if platform == "NT25":
                continue
            if platform == "NT3_ALPS" or platform == "NT3_LEO":
                url = f"https://hilreplay.nioint.com/api/bench/queue/pushcode?alps={info['code_branch']}"
            else:
                url = f"https://hilreplay.nioint.com/api/bench/queue/pushcode?replay={info['code_branch']}"
            data =[{
                "Name": info['host_ip'],
                "Hostname": info['hostname'],
                "CodeBranch": info['code_branch'],
            }]
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=600)
            print(response.text)
            response_data = json.loads(response.text)
            if response.status_code == 200 and response_data.get('success') and response_data.get('result').get(info['host_ip']):
                print(f"{platform}: Put code {info['test_queue_name']} success")
                self.check_result[platform]["put_code"] = True
                
            else:
                self.check_result[platform]["put_code"] = False
                raise Exception(f"{platform}: Put code {info['test_queue_name']} failed, status code: {response.status_code}")

    def bundle_valid(self):
        ## 判断bundle是否过期
        for platform, info in self.env_info.items():
            if platform == "NT25":
                continue
            bundle_url = info['bundle_url']
            if bundle_url:
                response = requests.head(bundle_url, timeout=20)  # 用 HEAD 请求只拿 header 更高效
                if response.status_code == 200:
                    print(f"{platform}: Bundle {bundle_url} is valid")
                    self.check_result[platform]["bundle_valid"] = True
                else:
                    self.check_result[platform]["bundle_valid"] = False
                    raise Exception(f"{platform}: Bundle {bundle_url} is invalid, status code: {response.status_code}")
            else:
                self.check_result[platform]["bundle_valid"] = False
                raise Exception(f"{platform}: Bundle {bundle_url} is empty")

    def send_test_task(self):
        for platform, info in self.env_info.items():
            if platform == "NT25":
                continue
            bundle_url = info['bundle_url']
            ## 共有参数
            common_parameters = {
                "name": f"test_code-{platform}-{datetime.now().strftime('%Y%m%d')}",
                "task_type": "test",
                "data_type": "dataMerge",
                "retry_count": 0,
                "muti_replay_percent": "100%",
                "priority": 1,
                "nt_type": "NT2",
                "scene_info": None,
                "fix_retry_task": False,
                "reproduce": False,
                "need_pnc_record": False,
                "is_general_task": True,
                "scale_job": None,
                "watchers": [
                    "new_mazu_builder",
                    "zhiming.guo2.o"
                ],
                "groups": [],
                "pass_rate": 1,
                "fail_rate": 0.5,
                "efficiency_hours": 8,
                "build_interval": 1,
                "author": "zhiming.guo2.o",
                "type": "hil_replay",
                "evaluate_params": "",
                "task_queue_name": ".",
                "task_front": 0.3,
                "checker_name": "",
                "config_name": "",
                "workflow_id": info["workflow_id"],
                }
            if platform == "NT2":
                data_parameters = {
                    "version": "master(dailysim)",
                    "scene_id": [
                        "692389",
                        "805843",
                        "182340"
                    ],
                    
                    "exec_config": f'{{"dms":false,"dlb_recall":true,"test_classification":"Daily",\
                        "backup_paths":["/home/mazu/app/conf"],"copy_mode":"trimmer_camera_udp","app_backup":false,"e2e":true,"hil_record":true,"retry":true,\
                        "mazu_debug_url":"{bundle_url}","patch_uuid":"18242418","dailysim_version":"master","nt_type":"NT2"}}',
                    }
            
            elif platform == "NT3_ALPS":
                data_parameters = {
                    "version": "stable/master_1orin_sud(dailysim)",
                    "scene_id": [
                        "194413",
                        "805841",
                        "692389",
                        "805843"
                    ],
                    "exec_config": f'{{"adviz":true,"drop_can":true,"checkers":["cpu_multiplex","map_info","replay_chain","time_multiplex","aes","aeb_brake_flag"],"process_lock":0,"soa_replay":true,"retry":false,"platform":"NT3_ALPS","nt_type":"NT2",\
                    "mazu_debug_url":"{bundle_url}","patch_uuid":"16625160",\
                    "dailysim_version":"stable/master_1orin_sud"}}',
                    }
            elif platform == "NT3_LEO":
                data_parameters = {
                    "version": "stable/leo_bl130(dailysim)",
                    "scene_id": [
                        "805842",
                        "692389",
                        "805843",
                        "752429"
                    ],
                    "exec_config": f'{{"adviz":true,"checkers":["leo_soc1_data","niomap"],"perception_od_confidence":true,"platform":"NT3_LEO","dlb_recall":true,"p1_leo_uds":true,\
                    "test_classification":"Daily","copy_mode":"trimmer_camera_udp","process_lock":0,"perception_god_confidence":true,"hil_record":true,"retry":true,\
                    "mazu_debug_url":"{bundle_url}","dailysim_version":"stable/leo_bl130","nt_type":"NT2"}}'
                }
                
            data_parameters.update(common_parameters)
            url = "http://adsim-metrics-api.nioint.com/metrics/hil_replay/new/job/save_run"
            response = requests.post(url, json=data_parameters)
            print(response.text)
            if response.status_code == 200 and json.loads(response.text).get('message') == "ok":
                print(f"{platform}:  Send test task  success: {json.loads(response.text).get('data', '')}, url: https://aip.nioint.com/#/adsim/hilReplay/management?page=0&task_queue_name=&created=-1&page_size=10&exec_plan_id={json.loads(response.text).get('data', '')}&author=zhiming.guo2.o")
                self.check_result[platform]["task_create_status"] = True
                self.check_result[platform]["send_test_task"] = json.loads(response.text).get('data', "")
            else:
                self.check_result[platform]["task_create_status"] = False
                self.check_result[platform]["send_test_task"] = ""
                raise Exception(f"{platform}: Send test task failed, status code: {response.status_code}")

        
    def select_task_exec_status(self):
        for platform, info in self.check_result.items():
            if platform == "NT25":
                continue
            if info["send_test_task"] != "":
                plan_id = info['send_test_task']
                task_queue = self.env_info[platform]["test_queue_name"]
                # plan_id = "68c91cfa5c4ae133cb375c6c"
                url = "http://adsim-metrics-api.nioint.com/metrics/hil_replay/new/table/list"
                data = {
                    "name": None,
                    "exec_plan_id": [
                        plan_id
                    ],
                    "task_type": None,
                    "priority": None,
                    "is_general_task": True,
                    "fix_retry_task": None,
                    "task_queue": task_queue,
                    "reproduce": None,
                    "need_pnc_record": None,
                    "created": -1,
                    "exec_status": None,
                    "author": [],
                    "page_size": "10",
                    "page": "0"
                    }
                response = requests.post(url, json=data)
                print(response.text)
                if response.status_code == 200:
                    result_data = response.json()['data']["content"]
                    for item in result_data:
                        print(f"{platform}:  Select task exec status: {item['exec_status']}")
                        self.check_result[platform]["task_exec_status"] = item['exec_status']
                        self.check_result[platform]["select_task_exec_status"] = True
                else:
                    self.check_result[platform]["select_task_exec_status"] = False
                    raise Exception(f"{platform}: Select task exec status failed, status code: {response.status_code}")

                
    def check_test_result(self):
        for platform, info in self.check_result.items():
            if platform == "NT25":
                continue
            plan_id = info['send_test_task']
            # plan_id = "68c91cfa5c4ae133cb375c6c"
            url = f"http://adsim-metrics-api.nioint.com/metrics/hil_replay/case/table_list?exec_plan_id={plan_id}&created=0&page_size=1000&page=0"
            response = requests.get(url)
            if response.status_code == 200:
                result_data = response.json()['data']
                print(f"{platform}:  Check test result success, status code: {response.status_code}")
            else:
                raise Exception(f"{platform}: Check test result failed, status code: {response.status_code}")
            # print(result_data)

            result_data['content']
            num = len(result_data['content'])
            for i in range(0, num):
                line = result_data['content'][i]
                case_id = line['case_id']
                try_num = len(line['common_fields'])
                for i in range(0, try_num):
                    task_id = line['common_fields'][i]['id']
                    checkers_result = line['common_fields'][i]['checkers_result']
                    if checkers_result.get("urban", "") == "":
                        continue
                    urban_pass_or_fail = checkers_result["urban"]['pass']
                    p0_issue_v2_pass_or_fail = checkers_result["P0_issue_v2"]['error']
                    if not urban_pass_or_fail or p0_issue_v2_pass_or_fail != "":
                        self.check_result[platform]["check_test_result"] = "fail"
                        send_alert_to_feishu(f"Check test result {platform} failed", f"https://aip.nioint.com/#/adsim/hilReplay/management/details?exec_plan_id={task_id}", case_id, platform, feishu_webhook_url)
                        break
                    else:
                        self.check_result[platform]["check_test_result"] = "pass"
                        send_alert_to_feishu(f"Check test result {platform} pass", f"https://aip.nioint.com/#/adsim/hilReplay/management/details?exec_plan_id={task_id}", case_id, platform, feishu_webhook_url)

        # for platform, info in self.check_result.items():
        #     if info["check_test_result"] == "pass":
        #         send_alert_to_feishu(f"Check test result {platform} pass", f"https://aip.nioint.com/#/adsim/hilReplay/management/details?exec_plan_id={task_id}", case_id, platform, feishu_webhook_url)


    def get_queue_host_id(self):
        for platform, info in self.env_info.items():
            queue_names = info['put_code_queue_name']
            group_names = info['put_code_group_name']
            for queue_name in queue_names:
                url = "https://hilreplay.nioint.com/api/BenchInfo/search?page=1&pageSize=50"
                data = {
                        "QueueName": queue_name
                        }
                response = requests.post(url, headers=self.headers, json=data, timeout=600)
                if response.status_code == 200:
                    result_data = response.json()['data']
                    for item in result_data:
                        print(f"{platform}:  Get queue host id, sucess")
                        self.env_info[platform]["all_hosts"].append({"Name":item['Name'], "Hostname": item['Hostname'], "CodeBranch": info['code_branch']})
                else:
                    raise Exception(f"{platform}: Get queue host id failed, status code: {response.status_code}")
                    

            for group_name in group_names:
                url = "https://hilreplay.nioint.com/api/BenchInfo/search?page=1&pageSize=50"
                data = {
                    "GroupName": group_name
                    }
                response = requests.post(url, headers=self.headers, json=data, timeout=600)
                if response.status_code == 200:
                    result_data = response.json()['data']
                    for item in result_data:
                        print(f"{platform}:  Get group host id, sucess")
                        self.env_info[platform]["all_hosts"].append({"Name":item['Name'], "Hostname": item['Hostname'], "CodeBranch": info['code_branch']})
                else:
                    raise Exception(f"{platform}: Get group host id failed, status code: {response.status_code}")
        print(self.env_info)
                
    def put_all_code(self):
        ## 每个台架都有一个id，我需要通过队列获取所有台架的id，然后在逐个进行推送代码
        for platform, info in self.env_info.items():
            ##  host_ids = [{'ID': 179, 'Name': '10.60.4.112', 'CodeBranch': 'dev'}, {'ID': 181, 'Name': '10.60.4.111', 'CodeBranch': 'dev'}]
            if platform == "NT3_ALPS" or platform == "NT3_LEO" or platform == "NT25":
                url = f"https://hilreplay.nioint.com/api/bench/queue/pushcode?alps={info['code_branch']}"
            else:
                url = f"https://hilreplay.nioint.com/api/bench/queue/pushcode?replay={info['code_branch']}"
            data = info['all_hosts']
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=3600)
            print(response.text)
            if response.status_code == 200 and json.loads(response.text).get('success'):
                print(f"{platform}: Put code success")
                ## 告警
            else:
                raise Exception(f"{platform}: Put code failed, status code: {response.status_code}")
                ## 告警

                    
        
    def recover_queue(self):
        for platform, info in self.env_info.items():
            if platform == "NT25":
                continue
            url = f"https://hilreplay.nioint.com/api/bench/queue/update?queueName={info['return_queue_name']}"
            data = [
                    {   
                        "ID": info['host_id'],
                        "Name": info['host_ip'],
                        "Hostname": info["hostname"],
                        "Resourcepool": "hil",
                        "QueueName": info['return_queue_name'],
                    }
                ]
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=300)
            print(response.text)
            if response.status_code == 200 and json.loads(response.text).get('success'):
                print(f"{platform}: Recover queue success")
                self.check_result[platform]["recover_queue"] = True
            else:
                self.check_result[platform]["recover_queue"] = False    
                raise Exception(f"{platform}: Recover queue failed, status code: {response.status_code}")

            



    def check(self):
        # 1. 先测试更新队列
        self.update_queue()
        

        ## 2. 推送测试代码
        self.put_code()
    
    
        ## 3. 检测bundle是否过期
        self.bundle_valid()
       

        ## 4. 发送测试任务
        self.send_test_task()

        ## 5. 检测任务执行状态
        summaty_time = 0
        for i in range(1, 10):
            print(f"正在检测任务状态... 第{i}次检测, 已运行时间: {summaty_time // 60 // 60}小时")
            self.select_task_exec_status()
            if self.check_result["NT2"]["task_exec_status"] != "FINISH" or self.check_result["NT3_ALPS"]["task_exec_status"] != "FINISH" or self.check_result["NT3_LEO"]["task_exec_status"] != "FINISH":
                    print(f"NT2: task exec status: {self.check_result['NT2']['task_exec_status']}")
                    print(f"NT3_ALPS: task exec status: {self.check_result['NT3_ALPS']['task_exec_status']}")
                    print(f"NT3_LEO: task exec status: {self.check_result['NT3_LEO']['task_exec_status']}")
                    time.sleep(30 * 60)
                    summaty_time += 30 * 60
                    if summaty_time >= 60 * 60 * 5:
                        print("任务执行超时，5小时未完成。")
                        return False
            else:
                print(f"NT2: task exec status: {self.check_result['NT2']['task_exec_status']}, 任务执行完成。")
                print(f"NT3_ALPS: task exec status: {self.check_result['NT3_ALPS']['task_exec_status']}, 任务执行完成。")
                print(f"NT3_LEO: task exec status: {self.check_result['NT3_LEO']['task_exec_status']}, 任务执行完成。")
                break
                
        # summaty_time = 0
        # for i in range(1, 10):
        #     print(f"正在检测任务状态... 第{i}次检测, 已运行时间: {summaty_time // 60 // 60}小时")
        #     self.select_task_exec_status()
        #     if self.check_result["NT2"]["task_exec_status"] != "EXEC":
        #             print(f"NT2: task exec status:", self.check_result["NT2"]["task_exec_status"])
        #             time.sleep(30 * 60)
        #             summaty_time += 30 * 60
        #             if summaty_time >= 60 * 60 * 5:
        #                 print("任务执行超时，5小时未完成。")
        #                 return False
        #     else:
        #         print(f"NT2: task exec status: {self.check_result['NT2']['task_exec_status']}, 任务执行完成。")
        #         break

        

   
        ## 6. 检测代码测试结果（check：urban等）
        self.check_test_result()
    
        ## 7. 获取台架id
        self.get_queue_host_id()
  
    
        # ## 8. 推送所有代码
        # self.put_all_code()
        
     
        ## 9. 恢复队列
        self.recover_queue()






test=TestCode()


test.check()



