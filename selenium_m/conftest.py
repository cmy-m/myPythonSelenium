#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

import pytest
from selenium_m.common.base_browser import BaseBrowser
from datetime import datetime
from py.xml import html
import allure
import base64
from selenium_m.common import constant

GL_BROWSER: BaseBrowser = None


# 定义一个全局的BaseBrowser对象，并且整个会话只创建一次对象
@pytest.fixture(scope='session', autouse=True)
def get_browser():
    print('会话前置, 开始启动浏览器')
    global GL_BROWSER
    GL_BROWSER = BaseBrowser()
    GL_BROWSER.get_url(url=constant.case_head[0]['url'])
    yield GL_BROWSER
    GL_BROWSER.quit()
    print('会话后置，开始关闭浏览器')


# 自定义addopts命令行参数,--as
def pytest_addoption(parser):
    """
    添加自定义命令行参数
    --添加是否打开失败截图的的命令行参数，默认no不打开，参数使用--ist=yes
    :param parser:
    """
    # 添加是否打开截图的的命令行参数，默认不开启，这里定义bool后回去参数异常，暂未定位到原因，先改成str类型？？？？？
    parser.addoption("--ist", action='store', default='no', type=str, choices=['yes', 'no'],
                     help="命令行参数，is_screenshot是否开启，默认不开启")


# 从pytest.ini配置文件中获取传入的参数
@pytest.fixture(scope='session')
def allure_screenshot(request):
    """
    获取自定义参数值的固件，可以通过固件传入用例中
    :param request:
    """
    yield request.config.getoption('--ist')


# @pytest.fixture(scope='session', autouse=True)
# def fun_return(pytestconfig):
#     # 可通过pytestconfig来获取命令行参数或者pytest.ini中的值
#     print('--------------------',pytestconfig.getini(name='--alluredir'))
#     yield


@pytest.fixture(scope='function')
def fun_function(fun_return):
    print('函数前置动作')
    yield fun_return + 1
    print('函数后置动作')


@pytest.fixture(scope='class')
def fun_class():
    print('类前置')
    yield
    print('类后置')


@pytest.fixture(scope='module')
def fun_module():
    print('模块前置')
    yield
    print('模块后置')


@pytest.fixture(scope='package')
def fun_package():
    print('包前置')
    yield
    print('包后置')


@pytest.fixture(scope='session')
def get_start_url():
    print('会话前置/////////')
    yield
    print('会话后置////////')


# 编辑报告标题
def pytest_html_report_title(report):
    report.title = "My very own title!"


# 运行测试前修改环境信息
def pytest_configure(config):
    config._metadata["foo"] = "bar"
    config._metadata.pop('Python')


# # 运行测试后修改环境信息
# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionfinish(session, exitstatus):
#     session.config._metadata["foo"] = "bar"


# 编辑摘要信息
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("foo: bar")])


@pytest.hookimpl(optionalhook=True)
# 测试结果表格
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop(2)
    cells.insert(2, html.th("Test_Name", class_="sortable desc", col="desc"))
    cells.pop()


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
    cells.pop(2)
    cells.insert(2, html.td(report.Test_name))
    cells.pop()


@pytest.hookimpl(optionalhook=True)
def pytest_collection_modifyitems(items):
    """解决pytest-html报告中文乱码问题，避免修改pytest-html/plugi.py源码"""
    mark_list = ['用例4']
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
        for x in mark_list:
            if x in item.name.encode('utf8').decode('unicode-escape'):
                print("//////////////////")
                item.add_marker(eval("pytest.mark.{}".format('nihao')))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    通过钩子函数处理运用时各阶段的数据
    :param item: 测试用例对象
    :param call: 测试用例执行阶段，setup， call， teardown
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    # 获取钩子函数的调用结果，返回一个result对象
    outcome = yield
    # report拿到用例执行结果的详情，从钩子方法的调用结果中获取测试报告
    report = outcome.get_result()
    # 自定义的列需要在这里进行赋值
    report.Test_name = str(item.function.__doc__)
    # extra = getattr(report, "extra", [])

    if report.when == "call" or report.when == "setup":
        fixture_extras = getattr(item.config, "extras", [])
        plugin_extras = getattr(report, "extra", [])

        # 执行失败进行截图
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            if item.config.getoption('--ist') == 'yes':
                file_name = report.nodeid.replace("::", "_") + ".png"
                screen_img = _capture_screenshot()
                if file_name:
                    html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                    plugin_extras.append(pytest_html.extras.html(html))
        report.extra = fixture_extras + plugin_extras


def _capture_screenshot():
    """
    截图保存为base64，兼容allure和html
    :return:
    """
    img = GL_BROWSER.driver.get_screenshot_as_base64()

    allure.attach(body=base64.b64decode(img), name='失败截图', attachment_type=allure.attachment_type.PNG)
    return img
