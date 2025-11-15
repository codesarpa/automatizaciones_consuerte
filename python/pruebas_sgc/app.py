from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright
import re
import logging
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
import time


# playwright = sync_playwright().start()
# browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
# page = browser.new_page()
# page.goto("http://10.231.0.137/consuertepruebas/")


# context = browser.new_context(
#     http_credentials={"username": "bill", "password": "pa55w0rd"}
# )
# page = context.new_page()
# page.goto("https://example.com")

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
context = browser.new_context(
    http_credentials={"username": "CP1029980182", "password": "123"}
)
page = context.new_page()
page.goto("http://10.231.0.137/consuertepruebas/")

# Diligencia solo una vez
page.get_by_label("Username or email address").fill("username")
page.get_by_label("Password").fill("password")
page.get_by_role("button", name="Sign in").click()

# Guarda sesi�n
context.storage_state(path="sesion.json")

input("HOLA")