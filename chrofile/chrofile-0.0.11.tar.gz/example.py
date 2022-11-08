import re
from time import sleep
from chrofile.core import chrofile
from lxml import html 
from pydash.objects import get
from selenium.webdriver.common.by import By

if __name__ == "__main__":
  store_id = 'twisnu2727'
  driver = None
  records = []
  start_urls = [f'https://www.tokopedia.com/{store_id}/etalase/sold']
  try:
    driver = chrofile()
    driver.get(start_urls[0])
    while True:
      sleep(3)
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
      sleep(2)
      source = html.fromstring(driver.page_source) 
      for product in source.xpath("//div[contains(@class, 'prd_container-card')]"):
        records.append({
          'url': get(product.xpath(".//a[contains(@class, 'pcv3__info-content')]/@href"), '[0]', None),
          'store_id': store_id,
          'image': get(product.xpath(".//img[@data-testid='imgProduct']/@src"), '[0]', None),
          'name': get(product.xpath(".//div[contains(@class, 'prd_link-product-name')]/text()"), '[0]', ''),
          'price': int(re.sub(r'\D', '', get(product.xpath(".//div[contains(@class, 'prd_link-product-price')]/text()"), '[0]', None)) or '0'),
          'currency_id': 'rp',
          'rate': float(get(product.xpath(".//span[contains(@class, 'prd_rating-average-text')]/text()"), '[0]', None) or '0'),
          'sold': int(re.sub(r'\D', '', get(product.xpath(".//span[contains(@class, 'prd_label-integrity')]/text()"), '[0]', None)) or '0')
        })
      
      next_button = get(driver.find_elements(By.XPATH, ("//a[@data-testid='btnShopProductPageNext']")), '[0]', None)
      
      if not next_button : break
      next_button.click()
      driver.execute_script("window.scrollTo(0, 0)")
      
    print(records)
  except Exception as e:
    print(e)
  finally:
    if driver: driver.quit()