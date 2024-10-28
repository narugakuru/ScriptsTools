import requests

url = "http://127.0.0.1:8000/run_script/test_script"
params = {
    "origin_path": "Z:\\ssl-htdocs",
    "copy_path": "E:\\WorkSpace\\WebKaisyu\\html_1024",
    "file_list": [
        "common/css/common.css",
        "jbaudit/target/02.html",
        "jbaudit/target/04.html",
        "jbaudit/target/05.html",
        "jbaudit/target/06.html",
        "effort/flow.html",
        "effort/operation/index.html",
        "/pr/kensa/activity/demand_r04_02.html",
        "common2/css/english.css",
        "english/index.html",
        "english/template/footer.php",
        "common/template/footer.php",
        "common2/tmp/footer.php",
        "common2/css/basic.css"
    ]
}

response = requests.post(url, json=params)
print(response.json())