# Copyright 2020 TestProject (https://testproject.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from packaging import version
from src.testproject.helpers import ConfigHelper
from src.testproject.sdk.drivers import webdriver
from selenium.webdriver import ChromeOptions
from tests.pageobjects.web import LoginPage, ProfilePage

if version.parse(ConfigHelper.get_sdk_version()) < version.parse("0.64.0"):
    pytest.skip("This feature is not supported in SDK versions < 0.64.0", allow_module_level=True)


@pytest.fixture
def driver():
    chrome_options = ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(chrome_options=chrome_options, project_name="CI - Python")
    yield driver
    driver.quit()


def test_update_profile_expect_success_message_to_be_displayed(driver):

    LoginPage(driver).open().login_as("John Smith", "12345")
    ProfilePage(driver).update_profile(
        country="Australia",
        address="Main Street 123",
        email="john@smith.org",
        phone="+1987654321",
    )
    assert ProfilePage(driver).saved_message_is_displayed()


def test_update_profile_again_expect_success_message_to_be_displayed(driver):

    LoginPage(driver).open().login_as("Bob Jones", "12345")
    ProfilePage(driver).update_profile(
        country="Canada",
        address="Maple Street 456",
        email="bob@jones.org",
        phone="+1123456789",
    )
    assert ProfilePage(driver).saved_message_is_displayed()
