from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class TestWebpage(unittest.TestCase):
    board_url="https://wriddle.vercel.app/?test=yes"
    transition_time=3

    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)

        service = webdriver.ChromeService(executable_path = '/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_title(self):
        self.driver.get(self.board_url)

        self.assertEqual(self.driver.title, "Wriddle")
    
    def test_invalid_word(self):
        self.driver.get(self.board_url)

        letters = list('abbac')
        for letter in letters:
            button = self.driver.find_element(By.XPATH, (f"//button[text()='{letter}']"))
            button.click()

        buttons = self.driver.find_elements(By.CLASS_NAME, 'keyboard-command')
        buttons[1].click()

        element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Sorry, abbac is not a word')]")))
        self.assertEqual(element.text, 'Sorry, abbac is not a word')
   
    def test_all_wrong_letters(self):
        self.driver.get(self.board_url)

        letters = list('adieu')
        for letter in letters:
            button = self.driver.find_element(By.XPATH, (f"//button[text()='{letter}']"))
            button.click()

        buttons = self.driver.find_elements(By.CLASS_NAME, 'keyboard-command')
        buttons[1].click()
        
        time.sleep(self.transition_time)
        tiles = self.driver.find_elements(By.CLASS_NAME, 'character')

        for tile in tiles[0:5]:
            self.assertEqual(tile.value_of_css_property('background-color'), 'rgba(0, 0, 0, 1)')

    def test_correct_word(self):
        self.driver.get(self.board_url)

        letters = list('jolly')
        for letter in letters:
            button = self.driver.find_element(By.XPATH, (f"//button[text()='{letter}']"))
            button.click()

        buttons = self.driver.find_elements(By.CLASS_NAME, 'keyboard-command')
        buttons[1].click()

        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'YOU WIN')]")))

        time.sleep(self.transition_time)
        tiles = self.driver.find_elements(By.CLASS_NAME, 'character')

        for tile in tiles[0:5]:
            self.assertEqual(tile.value_of_css_property('background-color'), 'rgba(0, 128, 0, 1)')

    def tearDown(self):
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()