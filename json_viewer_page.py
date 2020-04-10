from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, invisibility_of_element_located


"""
Represents a generic web page with basic functionality wrappers for WebDriver
"""
class WebPage(object):
    def __init__(self, driver):
        self.driver = driver

    def _get_element(self, xpath=None, css_selector=None):
        if xpath:
            return self.driver.find_element(By.XPATH, xpath)
        elif css_selector:
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)
        else:
            raise Exception("Don't know how to select the element")

    def _get_element_locator(self, xpath=None, css_selector=None):
        if xpath:
            return By.XPATH, xpath
        elif css_selector:
            return By.CSS_SELECTOR, css_selector
        else:
            raise Exception("Don't know how to locate the element")

    def _wait_for(self, condition, timeout=60):
        WebDriverWait(self.driver, timeout).until(condition)

    def _wait_for_element_presence(self, xpath=None, css_selector=None, timeout=60):
        locator = self._get_element_locator(xpath, css_selector)
        self._wait_for(presence_of_element_located(locator), timeout)

    def _wait_for_element_disappearance(self, xpath=None, css_selector=None, timeout=60):
        locator = self._get_element_locator(xpath, css_selector)
        self._wait_for(invisibility_of_element_located(locator), timeout)

    def _input_text(self, xpath=None, css_selector=None, text=""):
        input_field = self._get_element(xpath, css_selector)
        input_field.send_keys(text)

    def _click(self, xpath=None, css_selector=None):
        button = self._get_element(xpath, css_selector)
        button.click()


"""
Represents the main page of http://jsonviewer.stack.hu
"""
class JsonViewPage(WebPage):
    def __init__(self, driver=webdriver.Chrome(), url="http://jsonviewer.stack.hu"):
        super(JsonViewPage, self).__init__(driver)
        self.driver.get(url)

    def load_json_from_url(self, url):
        LOAD_JSON_BUTTON_XPATH = '//button[@class="x-btn-text" and text()="Load JSON data"]'
        INPUT_URL_CSS_SELECTOR = 'div.x-window  div.x-form-element input'
        SUBMIT_URL_XPATH = '//button[@type="button" and text()="Load JSON data!"]'
        LOADING_OVERLAY_CSS_SELECTOR = 'div.ext-el-mask'

        self._wait_for_element_presence(xpath=LOAD_JSON_BUTTON_XPATH)
        self._click(xpath=LOAD_JSON_BUTTON_XPATH)
        self._wait_for_element_presence(css_selector=INPUT_URL_CSS_SELECTOR)
        self._input_text(css_selector=INPUT_URL_CSS_SELECTOR, text=url)
        self._click(xpath=SUBMIT_URL_XPATH)
        self._wait_for_element_disappearance(css_selector=LOADING_OVERLAY_CSS_SELECTOR)

    def format_json(self):
        FORMAT_BUTTON_XPATH = '//button[@class="x-btn-text" and text()="Format"]'

        self._wait_for_element_presence(xpath=FORMAT_BUTTON_XPATH)
        self._click(xpath=FORMAT_BUTTON_XPATH)

    def get_json_text(self):
        TEXT_EDITOR_CSS_SELECTOR = 'textarea#edit'

        text_editor = self._get_element(css_selector=TEXT_EDITOR_CSS_SELECTOR)
        return text_editor.get_attribute('value')

    def switch_to_viewer(self):
        VIEWER_BUTTON_XPATH = '//span[@class="x-tab-strip-text " and text()="Viewer"]'

        self._wait_for_element_presence(xpath=VIEWER_BUTTON_XPATH)
        self._click(xpath=VIEWER_BUTTON_XPATH)

    def get_error_message(self, timeout=5):
        ERROR_DIALOG_CSS_SELECTOR = 'div.x-window.x-window-dlg'
        ERROR_TEXT_CSS_SELECTOR = 'span.ext-mb-text'

        try:
            self._wait_for_element_presence(css_selector=ERROR_DIALOG_CSS_SELECTOR, timeout=timeout)
        except TimeoutException:
            return None

        return self._get_element(css_selector=ERROR_TEXT_CSS_SELECTOR).text
