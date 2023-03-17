#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen
import pytest
import os

pytest.main()
os.system(r"cp ./config/environment.properties ./allure-results/environment.properties")
os.system(r"cp ./config/categories.json ./allure-results/categories.json")
os.system(r"allure generate -c -o allure-report")
