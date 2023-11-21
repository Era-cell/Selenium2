import os
import testing.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InformationExtractor(webdriver.Chrome):
    def __init__(self, driver_path=r"E:\RPA\Web_Automation", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        # add options for the chrome driver
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("detach", True)
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(InformationExtractor, self).__init__(options=opts)
        self.implicitly_wait(3)
        self.wait = WebDriverWait(self, 10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_details(self):
        self.get(const.BASE_URL)
        files_in_folder = [f for f in os.listdir() if f.startswith("output_file")]
        file_no = len(files_in_folder) + 1

        for i in range(5):
            ele_list = self.find_element(By.XPATH,
                                         '/html/body/div[2]/div[2]/div[2]/div/div[3]/div[6]/div/div/div/div[3]/div/table/tbody')
            ele_list = ele_list.find_elements(By.TAG_NAME, 'tr')
            element = ele_list[i]
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            element.find_elements(By.TAG_NAME, 'td')[1].find_element(By.TAG_NAME, 'a').click()
            val = self.find_element(By.XPATH,
                                    const.VAL_PATH).text
            print(val)
            desc = self.find_element(By.XPATH,
                                     const.DESC_PATH).text
            print('Description:', desc)
            addn_desc = self.find_element(By.XPATH,
                                          const.ADDN_DESC_PATH).text
            print('Additional description:', addn_desc)
            closing_date = self.find_element(By.XPATH,
                                             const.CLOSING_DATE_PATH).text
            dept = self.find_element(By.XPATH,
                                     const.DEPT_PATH).text
            dept = ' '.join(dept.split()[2:])
            print(f'Closing date of {dept} is:', ' '.join(closing_date.split()[3:]))

            
            # self.find_element(By.ID,
            #                   'id_prevnext_next').click()
            # --NEXT button was not given access and it was disabled so refreshing the page is an option
            self.refresh()

            # Store information in a file
            with open(f'output_file{file_no}.txt', 'a') as file:
                file.write(f'Value: {val}\n')
                file.write(f'Description: {desc}\n')
                file.write(f'Additional description: {addn_desc}\n')
                file.write(f'Closing date of {dept} is: {" ".join(closing_date.split()[3:])}\n')
                file.write('\n')
