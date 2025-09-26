# auto_test_code


## 1. 先测试更新队列
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

## 6. 检测代码测试结果（check：urban等）
self.check_test_result()

## 7. 获取台架id
self.get_queue_host_id()


# ## 8. 推送所有代码
# self.put_all_code()


## 9. 恢复队列
self.recover_queue()
