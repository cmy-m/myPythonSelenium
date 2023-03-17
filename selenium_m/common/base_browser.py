#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

from selenium_m.common.base_driver import BaseDriver
from selenium_m.lib import r_w_file
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_m.common import constant


class BaseBrowser(BaseDriver):
    def __init__(self):
        """
        读取selenium_webdriver的配置，如果没有获取到配置内容，就使用默认的chrome驱动
        :rtype: object
        """
        super().__init__()
        driver_ini = r_w_file.IniFile.read_ini(constant.driver_ini_path, 'driver')

        if len(driver_ini) > 0:
            self._driver_type = driver_ini['driver_type']
            self._wait = driver_ini['wait']
            self._driver_path = driver_ini['driver_path']
        try:
            self.driver = self._get_driver()
        except Exception as e:
            print('webDriver启动失败', e)

    def switch_new_window(self):
        """
        切换到最新页面
        """
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_iframe(self, locator, timeout=10):
        """
        切换iframe
        :param locator: iframe的属性
        :param timeout: 等待元素出现的最长时间，默认10秒
        """
        # iframe = self.browser.find_element(*locator)
        # self.browser.switch_to.frame(iframe)
        # 使用显性等待 切换 iframe
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_iframe_back(self):
        """
         从iframe 切回主页面
        """
        self.driver.switch_to.default_content()

    def switch_to_alter(self, option='accept', input_str=None):
        """
        处理三种alter弹窗
        :param option: 默认为点击取消， accept表示点击确定
        :param input_str: 弹窗为prompt类型时，需要输入的内容，默认为None
        """
        alter = self.driver.switch_to.alert
        if option == "accept":
            if input_str is not None:
                alter.send_keys(input_str)
            alter.accept()
        else:
            alter.dismiss()

    def get_alter_txt(self):
        """
        获取alter弹窗的文本信息
        :return:
        """
        return self.driver.switch_to.alert.text

    def scroll_to_bottom(self):
        """
         滚动到页面底部，使用js操作
        """
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def scroll_to_top(self):
        """
        滚动到页面顶部，使用js操作
        """
        js = "window.scrollTo(0,-document.body.scrollHeight)"
        self.driver.execute_script(js)

    def scroll_to_element(self, element):
        """
        将页面滚动到指定元素
        :param element: 查找到的元素 find_element后的元素
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def by_css(self, css_selector, is_list=False):
        """
        标签、属性、或者组合等定位
        css_selector格式：
            css用#表示ID，用 . 表示class，也可以直接使用名称，例如：#2等价于[id=2]， .miles等价于[class=miles]
            标签定位，直接用名称也支持标签层级，例如：div#2>span>input> 等价于 div[id=2]>span>input,
            其他组合，[属性名=属性值]
            多属性， div[id=2][class=miles]
            模糊查询，匹配开头^=  匹配结尾&=  匹配中间*=
        :param css_selector:
        :param is_list: 是否获取多个值， True代表是
        """
        # return self.driver.find_element_by_css_selector(css_selector)
        if is_list:
            return self.driver.find_elements(by=By.CSS_SELECTOR, value=css_selector)
        else:
            return self.driver.find_element(by=By.CSS_SELECTOR, value=css_selector)

    def by_xpath(self, xpath, is_list=False):
        """
        html中任意路径上的内容都可以作为定位手段
        xpath格式：
            "//*[@id='2']" 等价于 css中[id=2]
            "//div[@id='2']//span//input" 等价于 div[id=2]>span>input
            "//div[@id='2']/.." 选择div中ID=2的父节点（/..表示上级，可以多个），css无此写法
            "//div[@id='2' and name='miles']" 通过多属性值查找，支持 or css无此写法
            模糊查询， 匹配开头"//div[starts-with(@name, 'mi')], 匹配结尾 ends-with, 中间匹配 contains
            "//div[text()='更多']" 通过文本查找，标签div并且div标签的文本为更多
        :param xpath:
        :param is_list: 是否获取多个值， True代表是
        """
        # return self.driver.find_element_by_xpath(xpath)
        if is_list:
            return self.driver.find_elements(by=By.XPATH, value=xpath)
        else:
            return self.driver.find_element(by=By.XPATH, value=xpath)

    def by_id(self, id, is_list=False):
        """
        通过ID属性查找元素
        :param id: 属性值
        :param is_list: 是否查询多个，默认只查找第一个，True可以查找所有符合条件的元素
        :return:
        """
        if is_list:
            return self.driver.find_elements(by=By.ID, value=id)
        else:
            return self.driver.find_element(by=By.ID, value=id)

    def by_name(self, name, is_list=False):
        """
        通过name属性查找元素
        :param name: 属性值
        :param is_list: 是否查询多个，默认只查找第一个，True可以查找所有符合条件的元素
        :return:
        """
        if is_list:
            return self.driver.find_elements(by=By.NAME, value=name)
        else:
            return self.driver.find_element(by=By.NAME, value=name)

    def by_classname(self, classname, is_list=False):
        """
        通过classname属性查找元素
        :param classname: 属性值
        :param is_list: 是否查询多个，默认只查找第一个，True可以查找所有符合条件的元素
        :return:
        """
        if is_list:
            return self.driver.find_elements(by=By.CLASS_NAME, value=classname)
        else:
            return self.driver.find_element(by=By.CLASS_NAME, value=classname)

    def get_url(self, url):
        """
        请求url
        :param url:
        """
        self.driver.get(url=url)

    def quit(self):
        """
        退出关闭浏览器
        """
        self.driver.quit()

    def mouse_hover(self, element):
        """
        鼠标悬停在元素上
        :param element: 查找到的元素 find_element后的元素
        """
        ActionChains(self.driver).move_to_element(to_element=element).perform()

    def capture_screenshot(self):
        """
        截图保存为base64
        :return:
        """
        return self.driver.get_screenshot_as_base64()
