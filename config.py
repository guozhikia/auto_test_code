env_info = {
    "NT2": {
        "host_ip": "10.60.4.111",
        "host_id": 181,
        "hostname": "P-hlidc-HiL-mazu-111",
        "test_queue_name": "hil-replay-general-nt2-testcode-111",
        "workflow_id": 4380264,
        "code_branch": "dev",
        "bundle_url": "https://ad-artifactory.nioint.com/artifactory/ad-common-nt2-builds/NT2A/refs/tags/1.5.0-rc.1/59660/P0228609_ZZ_20250909_fw_16aed84_app_18242418_debug.encrypted.tar.gz",
        "put_code_queue_name":["hil-replay-general-flexible-nt2daily", "hil-replay-general-hourly","hil-replay-general-daily-d1", "hil-replay-general-mr-master", "hil-replay-general-mr-master-dev"],
        "put_code_group_name":["nt2-sample"],  ## 模糊匹配
        "return_queue_name": "hil-replay-general-hourly",
        "all_hosts": []
        },
    "NT3_ALPS": {
        "host_ip": "10.60.4.28",
        "host_id": 194,
        "hostname": "P-hlidc-HiL-DOM-4-028",
        "test_queue_name": "hil-replay-general-alps-testcode-28",
        "workflow_id": 4410178,
        "code_branch": "alps",
        "bundle_url": "https://ad-artifactory.nioint.com/artifactory/ad-nt3-Edge-ad_common_release/debug/ecc_encrypted_NT3-bundle-202507211849-CN-Debug_taishan_1orin_2.2.0-rc.2.2_fw_e47fef76_app_16625160.tar.gz",
        "put_code_queue_name":["hil-replay-general-alps-stress", "hil-replay-general-alps-basebundle", "hil-replay-general-alps-mr-bl120", "hil-replay-general-alps-e2e-mr"],
        "put_code_group_name":["nt3-alps-sample"],  ## 模糊匹配
        "return_queue_name": "hil-replay-general-alps-test",
        "all_hosts": []
        },
    "NT3_LEO": {
        "host_ip": "10.170.142.240",
        "host_id": 262,
        "hostname": "P-shtyl-HiL-NT3-240",
        "test_queue_name": "hil-replay-general-p1-testcode-240",
        "workflow_id": 4320279,
        "code_branch": "p1",
        "bundle_url": "https://ad-artifactory.nioint.com:443/artifactory/ad-nt3-Edge-ad_common_release/debug/ecc_encrypted_NT3-bundle-202509090308-CN-Debug_olympus_2p1_0.6.0-rc.7.6_fw_33001c40_app_18242420.tar.gz",
        "put_code_queue_name":["hil-replay-general-p1-test-daily-110-nt3", "hil-replay-general-p1-masterp1-mr", "hil-replay-general-p1-leo-mr-basebundle"],
        "put_code_group_name":["nt3-p1-sample"],  ## 模糊匹配
        "return_queue_name": "hil-replay-general-p1-test",
        "all_hosts": []
        },
    "NT25": {
        "code_branch": "p1",
        "put_code_queue_name":["hil-replay-general-nt25-daily"],
        "put_code_group_name":["nt2.5-sample"],  ## 模糊匹配,
        "all_hosts": []
        }
}

feishu_webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/63871227-dec7-401c-bd48-23e03b82baaa"