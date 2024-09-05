import pyautogui
import time
import datetime

buttons_img = './buttons' # Откуда берем скриншоты

time.sleep(5) # Время, чтобы свернуть окно питона

def click_simple(coord):
    '''Берем координаты области экрана и нажимаем мышкой в центр'''
    cent = pyautogui.center(coord)
    pyautogui.click(cent)

def focus_filename():
    '''Специальная функция для фокусировки на техническом файле.
    По неизвестной причине скрипт видит то один, то другой вариант'''
    coord = pyautogui.locateOnScreen('{}/filename1.png'.format(buttons_img))
    if coord: # Ищем на экране filename1.png, если нашли, то нажимаем туда
        click_simple(coord)
        return
    time.sleep(2)
    coord = pyautogui.locateOnScreen('{}/filename0.png'.format(buttons_img))
    if coord:
        click_simple(coord)
        return
    time.sleep(2)
    coord = pyautogui.locateOnScreen('{}/filename2.png'.format(buttons_img))
    if coord:
        click_simple(coord)
        return
    time.sleep(2)
    coord = pyautogui.locateOnScreen('{}/filename3.png'.format(buttons_img))
    if coord:
        click_simple(coord)
        return
    time.sleep(2)
    coord = pyautogui.locateOnScreen('{}/filename4.png'.format(buttons_img))
    if coord:
        click_simple(coord)
        return
    clk('filename0.png') # если не нашли ничего, переходим в цикл
        
def clk(button):
    '''функция для поиска на экране и нажимания произвольной кнопки'''
    while True: # бесконечный цикл, если вдруг сразу не нашли 
        coord = pyautogui.locateOnScreen('{}/{}'.format(buttons_img, button))
        if coord:
            break
        print('waiting '+button) # сообщаем в шелл, что все еще ждем кнопку
        time.sleep(3) # полезно дать компьютеру возможность подумать
    click_simple(coord) # нажимаем

time_previous_seconds = int(time.time()) # хочется посчитать среднее время на файл

# Для начала в FR уже должен быть открыт какой-то документ (!)

for x in range(1,1000): # цикл на 1000 файлов
    now = datetime.datetime.now() # чтобы ориентироваться по времени
    print(now.strftime("%H:%M:%S"))
    time_current_seconds = int(time.time()) # для подсчета среднего на файл
    avg = (time_current_seconds - time_previous_seconds) / x
    print('Avg per item: ', str(datetime.timedelta(seconds=avg)))
    print('New task ', x) # отмечаем, что беремся за новый файл
    time.sleep(5) # компьютер может ответить не сразу
    clk('new_task.png') # нажимаем на кнопку новой задачи
    time.sleep(3)
    # FR спросит, сохранить ли проект, нужно сказать "Нет".
    # Тут не сразу всё хорошо получалось, так что я вставил костыль с else:
    if pyautogui.locateOnScreen('{}/{}'.format(buttons_img, 'project_save_no.png')):
        clk('project_save_no.png')
    else:
        clk('new_task.png')
        if pyautogui.locateOnScreen('{}/{}'.format(buttons_img, 'project_save_no.png')):
            clk('project_save_no.png')
    time.sleep(20)
    print('Open file')
    clk('open_file.png') # нажимаем на кнопку "Открыть", чтобы загрузить файл
    time.sleep(15)
    #clk('filename1.png')
    #clk('filename0.png')
    focus_filename() # в директории лежит технический файл, нужно тыцнуть на него
    for _ in range(x): # нажимаем на стрелочку вправо столько раз, 
        pyautogui.press('right') # сколько файлов обработали
        
    print('file opening: ', x) # полезная инфа: какой это по счету файл в обработке

    time.sleep(3) 
    clk('open_button.png') # щелкаем по кнопке "Открыть"
    time.sleep(10) # на открытие нужно время
    clk('recognize.png') # щелкаем по кнопке "Распознать"
    first_time = int(time.time()) # запоминаем время начала
    print('Recognition task') # сообщаем, что идет распознавание,
    # удобный момент, чтобы свернуть окно и выполнить какую-то другую задачу
    
    time.sleep(3)
    
    
    while True: # невозможно угадать, когда кончится распознавание
        if pyautogui.locateOnScreen('{}/{}'.format(buttons_img, 'close.png')):
            clk('close.png') # поэтому ищем сообщение о предупреждениях
            break # закрываем такое сообщение - это конец распознавания
        else:
            time.sleep(5) # FR может не выдать предупреждений :(
            later_time = int(time.time())
            diff = later_time - first_time
            if diff > 1800: # Дадим на распознавание 50 минут
                print('Sec. {}'.format(diff))
                break
    
    
    time.sleep(3)
    print('Save') # сохраняем результат как pdf с текстом
    clk('save_pdf.png')
    time.sleep(3)
    clk('save.png') # щелкаем по кнопке в файловом диалоге
    time.sleep(15)

    while True:
        #sv = pyautogui.locateOnScreen('{}/{}'.format(buttons_img, 'saving.png'))
        sv = pyautogui.locateOnScreen('{}/{}'.format(buttons_img, 'cancel.png'))
        if sv: # сохранение занимает время
            print('saving...') # проверяем, есть ли на экране кнопка "Отменить"
            time.sleep(15) # пока она есть, идет сохранение
        else: # кнопка исчезла, сохранение завершено
            print('saving ended')
            time.sleep(5)
            break

