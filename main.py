import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By

token = '5259692334:AAH65L1ci1E2d5-4Chkt_KuNIuLLHmg1XCQ'
bot = telebot.TeleBot(token)

def link(domen, page, driver, links):
    url = (f'{domen}&page={page}')
    driver.get(url)

    items = driver.find_elements(By.CLASS_NAME, "x-product-card__link")
    for item in items:
        link = item.find_element(By.CLASS_NAME, "x-product-card__pic-catalog").get_attribute('href')
        links.append(link)

        print(link)

@bot.message_handler(commands=['start'])
def parsing(message):
    domen = 'https://www.lamoda.ru/c/595/bags-muzhskie-ryukzaki/?zbs_content=js_m_icons_869376_ruua_2502_icon_m_fw21'
    pages = 21

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    bot.send_message(message.chat.id, 'Собираются ссылки')

    links = []
    for page in range(1, pages + 1):
       link(domen, page, driver, links)

    for url in links:
        driver.get(url)

        brand = driver.find_element(By.CLASS_NAME, 'product-title__brand-name').text
        price = driver.find_element(By.XPATH, "//span[@class='_1xktn17sNuFwy45DZmZ5Oe']").text
        article = driver.find_element(By.XPATH, "//div[@class='_1gS6CINkPfFCHn1wO8uNcu']//div//div[2]//p[1]//span").text

        bot.send_message(message.chat.id, f'Бренд: {brand}, цена: {price}, артикул: {article}, ссылка: {url}')


bot.polling()