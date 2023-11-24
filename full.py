from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
# 创建一个Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)

# 在这里添加你要访问的网页URL
url = "https://dxpx.uestc.edu.cn/"
driver.get(url)

# 等待URL包含"https://dxpx.uestc.edu.cn/user/account/info"
WebDriverWait(driver, 200).until(EC.url_contains("https://dxpx.uestc.edu.cn/user/account/info"))

new_url = "https://dxpx.uestc.edu.cn/jjfz/lesson"
driver.get(new_url)

# 设置一个等待时间，等待URL包含"https://dxpx.uestc.edu.cn/jjfz/lesson"
WebDriverWait(driver, 200).until(EC.url_contains("https://dxpx.uestc.edu.cn/jjfz/lesson"))
base_url = "https://dxpx.uestc.edu.cn/"
print("OK!")

# 设置一个等待时间，以便等待页面加载完全
wait = WebDriverWait(driver, 3)

try:

    # 找到class等于lesson_c_ul的ul元素
    ul_element = driver.find_element(By.CLASS_NAME, "lesson_c_ul")

    # 找到ul下的所有li元素
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

except TimeoutException as te:
    print("页面加载超时:", str(te))
except Exception as e:
    print("发生错误:", str(e))    
# 在外层循环之前计算并存储局部变量
study_a_url_list = []
first_dd_text_list = []
second_dd_text_list = []

for li in li_elements:
    try:
        dl = li.find_element(By.TAG_NAME, "dl")
        
        # 找到dl下的所有dd元素
        dd_elements = dl.find_elements(By.TAG_NAME, "dd")

        # 存储 study_a, first_dd_text 和 second_dd_text
        study_a = li.find_element(By.CLASS_NAME, "study")
        study_a_url = study_a.get_attribute("url")  # 获取study元素的url属性
        study_a_url_list.append(study_a_url)
        first_dd_text = dd_elements[0].text.strip()[-1]
        first_dd_text_list.append(first_dd_text)
        second_dd_text = dd_elements[1].text.strip()[-1]
        second_dd_text_list.append(second_dd_text)
    except Exception as e:
        print("for li in li_elements循环发生错误:", str(e))  

for i in range(len(li_elements)):
    study_a_url = study_a_url_list[i]  # 获取存储的url属性
    first_dd_text = first_dd_text_list[i]
    second_dd_text = second_dd_text_list[i]

    li_b_text =  []
    new_url_b = []
        
    # 如果两个数字不相等
    if first_dd_text != second_dd_text:
        # 获取li下class为study的a标签的URL
        try:
            new_url = study_a_url
            # 将当前URL和new_url拼接在一起
            
            full_url = urljoin(base_url, new_url)
        
            # 打开新的网页B
            driver.execute_script("window.open('about:blank', 'new_tab');")
            driver.switch_to.window("new_tab")
            driver.get(full_url)
            
            # 在新的网页B中点击内部文本为“必修”的a标签
            must_link = driver.find_element(By.XPATH, "//a[text()='必修']")
            must_link.click()
            
            # 读取class为lesson1_lists的div下的ul下的所有li标签
            lesson1_lists = driver.find_element(By.CLASS_NAME, "lesson1_lists")
            li_elements_b = lesson1_lists.find_elements(By.TAG_NAME, "li")
        except Exception as e:
            pass
        li_len = len(li_elements_b)
        for li_b in li_elements_b:
            try:
                lesson_pass_div = li_b.find_element(By.CLASS_NAME, "lesson_pass")
                li_b_text.append(True)
            except NoSuchElementException:
                li_b_text.append(False)


            a_b = li_b.find_element(By.TAG_NAME, "a")
            new_url_ = a_b.get_attribute("href")
            new_url_b.append(new_url_)

        #可能有多页
        try:
            pages = lesson1_lists.find_element(By.CLASS_NAME,"pages")
            #一直点下一页，记录所有的课程
            while True:
                try:                    
                    next_page = pages.find_element(By.XPATH,"//a[text()='下一页']")
                    next_page.click()
                except NoSuchElementException:
                    break
                lesson1_lists = driver.find_element(By.CLASS_NAME, "lesson1_lists")
                _li_elements_b = lesson1_lists.find_elements(By.TAG_NAME, "li")
                li_len += len(_li_elements_b)
                for li_b in _li_elements_b:
                    try:
                        lesson_pass_div = li_b.find_element(By.CLASS_NAME, "lesson_pass")
                        li_b_text.append(True)
                    except NoSuchElementException:
                        li_b_text.append(False)


                    a_b = li_b.find_element(By.TAG_NAME, "a")
                    new_url_ = a_b.get_attribute("href")
                    new_url_b.append(new_url_)
                pages = lesson1_lists.find_element(By.CLASS_NAME,"pages")

        except NoSuchElementException:
            pass
        
        # print("li_b_text:" + str(li_b_text))
        # print("new_url_b" + str(new_url_b))
        for j in range(li_len):
            # 检查li_b标签内部是否包含“完成”的文本
            if li_b_text[j]:
                print("已完成一个课程！") 
                continue  # 如果包含“完成”，跳过此li
            else:
                # 拼接li_b标签下的a标签的href属性和当前URL，得到新地址
                
                full_url_b = urljoin(base_url, new_url_b[j])
                
                # 打开一个新窗口
                driver.execute_script("window.open('about:blank', 'new_tab_b');")
                driver.switch_to.window("new_tab_b")
                driver.get(full_url_b)
                print("开始看视频")
                # 在新窗口执行你的脚本
                while True:
                    all_li_red = True  # 标志，假设所有li的style属性都包含"red"
                    try:
                        # 使用Selenium的Expected Conditions来等待直到"继续"按钮可点击
                        continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "public_submit")))
                        
                        # 获取按钮的文本
                        button_text = continue_button.text
                        
                        # 如果按钮文本是"继续"，就点击按钮
                        if button_text == "继续":
                            print("继续！")
                            continue_button.click()
                    except Exception as e:
                        # 如果没有找到"继续"按钮或出现其他错误，可以在这里进行处理
                        pass

                    try:
                        # 使用Selenium的Expected Conditions来等待直到"继续"按钮可点击
                        continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "public_cancel")))
                        
                        # 获取按钮的文本
                        button_text = continue_button.text
                        
                        # 如果按钮文本是"继续"，就点击按钮
                        if button_text == "继续观看":
                            print("继续观看！")
                            continue_button.click()
                    except Exception as e:
                        # 如果没有找到"继续"按钮或出现其他错误，可以在这里进行处理
                        pass
                    # 获取class为"video_lists"的div元素
                    video_lists_div = driver.find_element(By.CLASS_NAME, "video_lists")
                    # 在class为"video_lists"的div元素内部查找ul元素
                    ul = video_lists_div.find_element(By.TAG_NAME, "ul")

                    # 获取ul下的所有li标签
                    li_elements_c = ul.find_elements(By.TAG_NAME, "li")
                    try:
                        # 使用Selenium的Expected Conditions来等待直到"我知道了"按钮可点击
                        know_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='我知道了']")))
                        print("我知道了")
                        # 点击"我知道了"按钮
                        know_button.click()
                    except Exception as e:
                        # 如果没有找到"我知道了"按钮、li标签或出现其他错误，可以在这里进行处理
                        pass
                    try:    
                        # 遍历li标签
                        for li in li_elements_c:
                            # 获取li标签下的a标签
                            a_element = li.find_element(By.TAG_NAME, "a")

                            # 获取a标签的style属性
                            style = a_element.get_attribute("style")
                            # print(style)
                            
                            # 如果style属性中不包含"red"，点击该li标签
                            if "red" not in style and "video_red" in li.get_attribute("class"):
                                break
                            elif "video_red" not in li.get_attribute("class") and "red" not in style:
                                print("下一个视频！")
                                li.click()
                                break  # 点击第一个符合条件的li标签后，退出循环                  
                        
                    except Exception as e:
                        # 如果没有找到"我知道了"按钮、li标签或出现其他错误，可以在这里进行处理
                        pass
                    try:
                        for li in li_elements_c:
                            # 获取li标签下的a标签
                            a_element = li.find_element(By.TAG_NAME, "a")

                            # 获取a标签的style属性
                            style = a_element.get_attribute("style")
                            # print(style)
                            
                            if "red" not in style:
                                all_li_red = False
                    except Exception as e:
                        continue

                    if all_li_red:
                        break
                
                print("结束！")
                
                # 关闭新窗口
                driver.close()
                driver.switch_to.window("new_tab")  # 切回到B页面
    else:
        print("一个部分已完成！")            
            
# 关闭WebDriver（可以根据你的需要在某个条件下结束循环后关闭）
driver.quit()
