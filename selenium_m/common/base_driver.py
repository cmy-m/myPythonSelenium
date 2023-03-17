#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

from selenium import webdriver
from lib import logguru
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.safari.service import Service as safari_service
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.ie.service import Service as ie_service
from selenium.webdriver.edge.service import Service as edge_service
# import chardet


class BaseDriver(object):

    _driver: webdriver = None

    def __init__(self):
        """
        设置默认浏览器为chrome，默认等待时长0秒，默认chrome的driver路径
        """
        self._driver_type = ''
        self._wait = 0
        self._driver_path = ''
        # self._driver: webdriver = webdriver.Chrome()

    def _get_driver(self):
        """
        根基配置获取对应的webdriver(默认chrome)
        并设置隐式等待
        :return: 返回一个selenium.webdriver对象
        """
        # global driver
        if self._driver_type == '':
            self._driver = webdriver.Chrome()

        if self._driver_type.lower() in ['chrome']:
            # 驱动路径新版本需要通过service传递
            self._driver = webdriver.Chrome(service=chrome_service(self._driver_path))
        elif self._driver_type.lower() in ["safari"]:
            self._driver = webdriver.Safari(service=safari_service(self._driver_path))
        elif self._driver_type.lower() in ["firefox"]:
            self._driver = webdriver.Firefox(service=firefox_service(self._driver_path))
        elif self._driver_type.lower() in ["edge"]:
            self._driver = webdriver.Edge(service=edge_service(self._driver_path))
        elif self._driver_type.lower() in ["ie"]:
            self._driver = webdriver.Ie(service=ie_service(self._driver_path))
        else:
            logguru.get_logguru().debug("browser_type is error")

        if self._driver is None:
            raise ValueError('selenium.webdriver对象获取异常，请检查web drive配置文件')
        self._driver.implicitly_wait(self._wait)
        return self._driver
