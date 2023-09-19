from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def main():
    
    NUMBER_TICKETS = 2
    
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://resale-aus.fwwc23.tickets.fifa.com/secured/selection/resale/item?performanceId=10228543141436&productId=101397765775&lang=en'

    time.sleep(1)
    driver.get(url)
    
    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, 'onetrust-reject-all-handler')))
    driver.find_element(By.ID, 'onetrust-reject-all-handler').click()
    
    block = -1
    seat_row = ""
    seat = -1
            
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.select('tr[id]')
        
        for row in rows:
                        
            if row.select_one('.resale-item-action'):
                ticket_type = row.select_one('td.resale-item-subCategory.tariff').get_text(strip=True)
                if ticket_type == "Adult":
                    ticket_location = row.select_one('td.resale-item-seatPath.seatPath').get_text(strip=True)
                    
                    if "Block" not in ticket_location:
                        split_string = ticket_location.split(" - ")
                        current_block = split_string[1]
                        current_row = split_string[2]
                        current_seat = int(split_string[3])
                        
                        row_id = row['id']
                        xpath_expression = f"//tr[@id='{row_id}']/td[@class='resale-item-action']/span[@class='button']/a[1]"
                        driver.find_element(By.XPATH, xpath_expression).click()
                        
                        if current_block != block or current_row != seat_row or current_seat - 1 != seat:
                            sum_seats = 1
                            # passs
                        
                        else:
                            sum_seats += 1
                            if sum_seats == NUMBER_TICKETS:
                                checkout_xpath = "//div[@id='controls']/span[@class='button add']/a[1]"
                                driver.find_element(By.XPATH, checkout_xpath).click()
                                while True:
                                    pass

                        block = current_block
                        seat_row = current_row
                        seat = current_seat
            
        driver.refresh()

if __name__ == '__main__':
    main()
