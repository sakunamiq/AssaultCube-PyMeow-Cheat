import pyMeow as pm
import os
from colorama import Fore
import time
from render import overlay

def main():
    os.system("cls")
    print('[+] by sakurai', '\n')
    print('[+] Загрузка оффсетов...')
    try:
        from offsets import health, armor, team, pos, fpos, name, player_count, entity_list, local_player, view_matrix
    except:
        print(Fore.RED + '[-] Оффсеты не найдены.')
        time.sleep(3)
        exit()
    print(Fore.GREEN + '[+] Оффсеты загружены.')
    time.sleep(0.5)
    print(Fore.WHITE + '[+] Проверяем, запущена ли игра...')
    
    if not pm.process_exists('ac_client.exe'):
        print(Fore.RED + '[-] Игра не запущенна.')
        time.sleep(3)
        exit()
    print(Fore.GREEN + '[+] Найден ac_client.exe', '\n')
    
    print(Fore.WHITE + '[+] Получение базового адреса модуля...')
    from memory import AccessGame
    try: 
        proc, base = AccessGame()
    except:
        print(Fore.RED + '[-] Базовый адрес модуля не найден...')
        time.sleep(3)
        exit()
      
    print(Fore.GREEN + '[+] Базовый адрес модуля:', base)
    print(Fore.WHITE + '[+] Загрузка оверлея...', '\n')
    
    overlay()
    
main()
    