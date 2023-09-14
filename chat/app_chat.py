from appium import webdriver
from time import sleep

# Appium连接参数
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '13',
    'deviceName': 'KRLRRKYD5H99A66D',
    'appPackage': 'cn.sharesmile.enjoychat',
    'appActivity': 'YOUR_APP_ACTIVITY'
}

# 启动App
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 等待App加载完成
sleep(5)
print(driver.current_package)
print(driver.current_activity)
# 定位消息输入框和发送按钮的元素ID或XPath
message_input = driver.find_element_by_id('message_input_id')
send_button = driver.find_element_by_id('send_button_id')

# 模拟自动回复
reply_message = "自动回复：收到消息，稍后回复。"
message_input.send_keys(reply_message)
send_button.click()

# 关闭App
driver.quit()
