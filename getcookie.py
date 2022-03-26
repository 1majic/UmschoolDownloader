from selenium_starter import StartUrlDriver
import pickle

driver = StartUrlDriver("https://umschool.net/")
input('После того как войдете в аккаунт - нажмите Enter: ')
pickle.dump(driver.get_cookies(), open("cookies", 'wb'))
input('Cookie сохранены! Нажмите Enter чтобы закрыть программу. ')
driver.close()
exit()