try:
    from selenium.webdriver.common.by import By

    from selenium_starter import StartUrlDriver, config
    import pickle
    import time

    from Class import Lesson

    import os
except Exception as e:
    print(e)
    input()


def beautify(block):
    text = block.name
    chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for i in chars:
        text = text.replace(i, '')
    return text


# Функция запуска браузера
def GetDriver(url):
    driver = StartUrlDriver(url)
    print("Загрузка cookies")

    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)
    return driver


def main():
    try:
        if os.listdir("files"):
            for i in os.listdir('files'):
                os.replace(f"files/{i}", f"Old/{i}")
    except:
        try:
            os.remove(f"files/{i}")
        except:
            pass
    # def GetLessons():
    driver = GetDriver("https://umschool.net/")
    time.sleep(1)
    print("Запуск страницы")
    driver.get("https://umschool.net/mastergroup/month/2264/lessons/")
    # Поиск блоков с уроком и запись их данных в экзепляр класса
    # while True:
    blocks = driver.find_elements(By.CLASS_NAME, "lessons-item")
    lessons = {}
    k = 0
    for lesson_block in blocks:
        try:
            button = lesson_block.find_element(By.CLASS_NAME, "btn-container")
            btn = button.find_element(By.CLASS_NAME, "button")
            if btn.text.lower() == 'посмотреть запись':
                les = Lesson(name=lesson_block.find_element(By.TAG_NAME, 'h2').text,
                             button=lesson_block.find_element(By.CLASS_NAME, "btn-container").find_element(
                                 By.TAG_NAME,
                                 "a").get_attribute("href"), materials=[i.get_attribute("href") for i in
                                                                        lesson_block.find_element(By.CLASS_NAME,
                                                                                                  "col-p-4").find_elements(
                                                                            By.TAG_NAME, "a")])
                lessons[str(k)] = les
                k += 1
        except:
            pass
    # Проецирование значений на экране
    for x, y in lessons.items():
        print(f"{x}. {y.name}")
    ranges = input('\nВыберите значения в формате формате диапозона "4-8" или через запятую: ').replace(' ',
                                                                                                        '').split(
        ',')

    pages = []
    for i in set(ranges):
        if '-' in i:
            rg = list(map(int, i.split('-')))
            for j in range(rg[0], rg[1] + 1):
                pages.append(str(j))
        else:
            pages.append(i)
    pages = sorted(pages)

    for i in pages:
        name = lessons[i].name
        driver.get(lessons[i].button)
        print(f'Загрузка "{name}"')

        try:
            link = driver.find_element(By.ID, "plyr_player_container").find_element(By.TAG_NAME,
                                                                                    "iframe").get_attribute(
                "src")
            link = link.split('?')[0].replace("embed/", "watch?v=")
        except:
            link = driver.find_element(By.ID, "plyr_player_container").find_element(By.TAG_NAME,
                                                                                    "iframe").get_attribute(
                "src")
            link = link.split('?')[0].replace("embed/", "watch?v=")
        lessons[i].link = link

        for j in lessons[i].materials:
            if ".pdf" in j:
                driver.get(j)
            else:
                driver.get(j)
                driver.get(f'{driver.current_url}?print')
                try:
                    extras = [_ for _ in driver.find_elements(By.CLASS_NAME, 'exercise-item')]
                    for l in extras:
                        l.find_element(By.CLASS_NAME, 'mb-3').find_element(By.TAG_NAME, 'a').click()
                    # extras = [i.click for i in driver.find_elements(By.CLASS_NAME, 'mb-3')]
                except Exception as e:
                    print(e)
                driver.execute_script('window.print();')

        time.sleep(5)
        while '.crdownload' in ' '.join(os.listdir('files')):
            time.sleep(1)
        for j in os.listdir('files'):
            l = 1
            if '.txt' not in j:
                try:
                    if '_' in j:
                        if not j[:j.index('_')].isdigit():
                            os.rename(f'files/{j}', f'files/{str(i)}_{j}')
                    else:
                        if 'Умскул – онлайн-школа ЕГЭ и ОГЭ.pdf' in j:
                            os.rename(f'files/{j}', f'files/{str(i)}_Дз.pdf')
                        else:
                            os.rename(f'files/{j}', f'files/{str(i)}_{j}')
                except FileExistsError:
                    os.rename(f'files/{j}', f'files/({l}){str(i)}_{j}')
                    l += 1
                except FileNotFoundError:
                    continue
        with open(f'files/{str(i)}_.txt', 'w') as file:
            file.write(f"{name}\n{link}")

    path = config['dest.fordler_directory'].replace("\\", "/")

    try:
        if os.listdir(f"{path}"):
            for i in os.listdir(f"{path}"):
                os.replace(f"{path}/{i}", f"Old/{i}")
    except:
        try:
            os.remove(f"{path}/{i}")
        except:
            pass

    for i in os.listdir('files'):
        ind = i.index('_')
        num = i[:ind]
        filename = i[ind + 1:]
        name = beautify(lessons[num])
        try:
            os.mkdir(f'{path}/{name}')
        except:
            pass
        if '.pdf' in i:
            os.rename(f'files/{i}', f'files/{filename}')
            os.replace(f'files/{filename}', f'{path}/{name}/{filename}')
        else:
            os.rename(f'files/{i}', f'files/text.txt')
            os.replace(f'files/text.txt', f'{path}/{name}/text.txt')


if __name__ == '__main__':
    main()
