#Программа для быстрого поиска и установки русификаторов

import os
import sys
import subprocess
import shutil
import requests
from ftplib import FTP
from pathlib import Path
from zipfile import ZipFile
import tkinter as tk
from tkinter import filedialog

local_dir = Path.home() / 'Documents' / 'Русификаторы'

root = tk.Tk()
root.withdraw()

 # ДЕЛАЕМ ОКНО ДИАЛОГА ПОВЕРХ ВСЕХ ОКОН
root.attributes('-topmost', True)  # Всегда поверх других окон
root.lift()  # Поднимаем наверх
root.focus_force()  # Принудительно устанавливаем фокус

hello_message = '''
Сделано: AngeloDeveD

Выберите игру для русификации:
1. Настройки

2. Final Fantasy 7 Remake
3. Final Fantasy 7 Rebirth
4. Final Fanatsy X-X2 (не работает)
5. Persona 5 Royal
6. Persona 4 Golden (не работает)

0. Выйти из программы

Прим.: Рекомендую отключить антивирусник, потому что иногда ошибочно выдаёт файлы руссификаторов как вирусы.
                         
Введите номер -> '''

class FF7_FTP:
    def __init__(self):
        self.ip = '78.36.10.56'
        self.port = 49143
        self.user = "mognet"
        self.passwd = "free"
        self.dir = '/public'
        self.__ftp = None
        self.__connected = False
    
    """Подключение к ftp серверу"""
    def connect_to_ftp(self):
        try:
            self.__ftp = FTP()
            self.__ftp.connect(self.ip, self.port, timeout=30)
            self.__ftp.login(user=self.user, passwd=self.passwd)
            self.__ftp.cwd(self.dir)
            self.__connected = True
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.__connected = False
            return False
    
    """Отключение от FTP сервера"""
    def disconnect(self):
        if self.__connected:
            try:
                self.__ftp.quit()
                self.__connected = False
                return True
            except Exception as e:
                print("Ошибка закрытия соединения с ftp: ", e)
                return False
        else:
            print("Вы не подключены к серверу")
            return True

    """Предоставление списка файлов"""
    def list_files(self):
        if self.__connected:
            return self.__ftp.nlst()
        else:
            print("Вы не подключены к ftp")
            return []
    """Установка файлов"""
    def download(self, filename, filepath):
        self.__ftp.retrbinary(f'RETR {filename}', filepath.write)
        return True
    
    def check_connection(self):
        return self.__connected

class Settings:
    def __init__(self):
        self.__path = Path.home() / 'Documents' / 'Русификаторы'
        self.__backup = True
        self.__createFolder = True

    """Отображае информацию параметров"""
    def ShowInfo(self):
        print(f"1. Резерваная копия: {self.__backup}")
        print(f"2. Местополоение руссификаторов: {self.__path}")

    """Даёт путь к папке с резервными копиями руссификаторов в формате Path"""
    def GetPath(self):
        return self.__path

    """Даёт путь к папке с резервными копиями руссификаторов в формате String"""
    def GetPathStr(self):
        return str(self.__path)
    
    """Назначает новую директорию для загрузки резервных копий руссификаторов"""
    def SetPath(self, newPath, createFolder="y"):
        if createFolder == 'y':
            self.__path(Path(newPath) / "Руссификаторы")
            self.__createFolder = True
        elif createFolder == 'n': 
            self.__path(Path(newPath))
            self.__createFolder = False
        else:
            print("Ошибка получения данных")
        return self.__createFolder
    
    """Возвращает значение на создане резервной копии"""
    def GetBackup(self):
        return self.__backup
        
    """Парамет для создания резервной папки с руссификаторами"""
    def SetBackup(self, options="y"):
        if options == "y": 
            self.__backup = True
        elif options == "n": 
            self.__backup = False
        else: 
            print("Ошибка получения данных")
        return self.__backup
    
    """Проверяет на наличие папки с резерными копиями. В случает отстутсвия создаст её."""
    def isFolderExist(self):
        if not self.__path.exists(): self.__path.mkdir()


settings = Settings()


"""Меню выбора игры"""
def menu():

    game = -1
    
    while game != 0:
        try:
            game = int(input(hello_message))
            found_rus(game)
        except Exception as e:
            print("Введено неверное значение!!", e)

    sys.exit()

"""Поиск последнего русификатора игры"""
def found_rus(id):

    settings.isFolderExist()

    #Параметы
    if id == 1:
        ShowSettings()
        print("Настройки успешно применены")

    #FF7 Remake
    if id == 2:
        title = 'Final Fantasy 7 Remake'
        ff7_ftp = FF7_FTP()
        ff7_ftp.connect_to_ftp()

        dir = ff7_ftp.list_files() #Получение списка файлов
        for file in dir:
            if "ff7r_" in file and "_steam.zip" in file:
                download_dir = settings.GetPath() / title # Создание директории под игру
                if not download_dir.exists(): download_dir.mkdir(exist_ok=True)

                file_path = download_dir / file
                with open(file_path, 'wb') as local_file:
                    print("Началась установка! Подождите...")
                    ff7_ftp.download(filename=file, filepath=local_file) #Сохранение файла в байтовом режиме
                print("Файл успешно установлен!!!")

                ArchiveZip(str(file_path), title) #Распаковка русификатора
                if settings.GetBackup() == False: 
                    try:
                        shutil.rmtree(settings.GetPath())
                        
                    except Exception as e:
                        os.rmdir(settings.GetPathStr())

                    finally:
                        print("Резервные копии удалены!")


        ff7_ftp.disconnect()
        if unzip_status == False and settings.GetBackup() == False:
            print("Руссификатор не установлен! Попробуйте включить резервную копию для ручной установки!")
        else:
            print("Руссификатор установлен!")
    
    #FF7 Rebirth
    elif id == 3:
        title = "Final Fantasy 7 Rebirth"
        ff7_ftp = FF7_FTP()
        ff7_ftp.connect_to_ftp()

        dir = ff7_ftp.list_files() #Получение списка файлов
        for file in dir:
            if "ff7r2_" in file and not "_translator.zip" in file:
                download_dir = settings.GetPath() / title # Создание директории под игру
                if not download_dir.exists(): download_dir.mkdir(exist_ok=True)

                file_path = download_dir / file
                with open(file_path, 'wb') as local_file:
                    print("Началась установка! Подождите...")
                    ff7_ftp.download(filename=file, filepath=local_file) #Сохранение файла в байтовом режиме
                print("Файл успешно установлен!!!")
                
                unzip_status = ArchiveZip(str(file_path), title) #Распаковка русификатора

                if settings.GetBackup() == False: 
                    try:
                        shutil.rmtree(settings.GetPath())
                        
                    except Exception as e:
                        os.rmdir(settings.GetPathStr())

                    finally:
                        print("Резервные копии удалены!")

        ff7_ftp.disconnect()

        if unzip_status == False and settings.GetBackup() == False:
            print("Руссификатор не установлен! Попробуйте включить резервную копию для ручной установки!")
        else:
            print("Руссификатор установлен!")

    #FFX-X2
    elif id == 4:
        title = "Final Fanatsy X-X2"

        #TODO
        url = r"https://downloader.disk.yandex.ru/disk/875a96107a42011da90a39b3ad3f0ea10bc790c4d744053141d81d465ed0c24b/69802278/WC3QgBY9DLIhNJvqkWR_z-IhYniU8Vj3Wy8Kl0k4JFK50wfV7wOJxLY_28uKLbMJsCNZzdrcQdCiHDU-r7m9lw%3D%3D?uid=0&filename=FFXRUS_PC.exe&disposition=attachment&hash=f5KX0D4W3wP%2B3ejUWAx9a/wXRhqO8abBGJY4w6wKSiQ%3D%3A/FFXRUS_PC.exe&limit=0&content_type=application%2Fx-msdownload&owner_uid=606074776&fsize=51346583&hid=aac7cbf8c88faa4c07c7efc7e28110d3&media_type=executable&tknv=v3"

        download_dir = settings.GetPath() / title # Создание директории под игру
        if not download_dir.exists(): download_dir.mkdir(exist_ok=True)

        filename = "FFX-X2.exe"

        file_path = download_dir / filename

        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Проверяем статус ответа

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        print(f"Размер файла: {total_size / 1024 / 1024:.2f} MB")
        print("Скачивание...")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Показываем прогресс если известен размер
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        sys.stdout.write(f"\rПрогресс: {percent:.1f}% ({downloaded/1024/1024:.2f}/{total_size/1024/1024:.2f} MB)")
                        sys.stdout.flush()
        
        if not file_path.exists():
            print("Руссификатор не установлен!")
            return None
        
        file_size = file_path.stat().st_size
        if file_size == 0:
            print("Руссификатор не установлен!")
            file_path.unlink()  # Удаляем пустой файл
            return None
        
        try:
            # Запускаем .exe файл
            subprocess.run([str(file_path)], check=False)
            print("\nПрограмма запущена!")
        except Exception as e:
                print(f"Ошибка при запуске: {e}")

    #P5R
    elif id == 5:
        title = "Persona 5 Royal"
        ff7_ftp = FF7_FTP()
        ff7_ftp.connect_to_ftp()

        dir = ff7_ftp.list_files() #Получение списка файлов
        for file in dir:
            if "p5r_" in file and "_steam.zip" in file:
                download_dir = settings.GetPath() / title # Создание директории под игру
                if not download_dir.exists(): download_dir.mkdir(exist_ok=True)

                file_path = download_dir / file
                with open(file_path, 'wb') as local_file:
                    print("Началась установка! Подождите...")
                    ff7_ftp.download(filename=file, filepath=local_file) #Сохранение файла в байтовом режиме
                print("Файл успешно установлен!!!")
                
                unzip_status = ArchiveZip(str(file_path), title) #Распаковка русификатора

                if settings.GetBackup() == False: 
                    try:
                        shutil.rmtree(settings.GetPath())
                        
                    except Exception as e:
                        os.rmdir(settings.GetPathStr())

                    finally:
                        print("Резервные копии удалены!")

        ff7_ftp.disconnect()

        if unzip_status == False and settings.GetBackup() == False:
            print("Руссификатор не установлен! Попробуйте включить резервную копию для ручной установки!")
        else:
            print("Руссификатор установлен!")

    #P4G
    elif id == 6:
        title = "Persona 4 Golden"
        
        #TODO
        url = r"https://downloader.disk.yandex.ru/zip/c4067c07057d5159668a67dba9921985f12620f06a44579b73366c77bb0a3590/697ff019/M2lhRGdkYVRvRWhuaUlZRVdaa2dBSHBDY3p0VWhvMVlrRWI3Y3NpVThjK0FMbDFuUFFWRWJnNE1uNnFHNC83Q3EvSjZicG1SeU9Kb25UM1ZvWG5EYWc9PQ==?uid=0&filename=%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%204%3A%20%D0%97%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%B5%20%D0%B8%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%28%D0%9F%D0%BE%D0%BB%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%2C%20%D0%9F%D0%B8%D1%80%D0%B0%D1%82%D0%BA%D0%B0%29.zip&disposition=attachment&hash=3iaDgdaToEhniIYEWZkgAHpCcztUho1YkEb7csiU8c%2BALl1nPQVEbg4Mn6qG4/7Cq/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&owner_uid=513217931&tknv=v3"

        download_dir = settings.GetPath() / title # Создание директории под игру
        if not download_dir.exists(): download_dir.mkdir(exist_ok=True)

        filename = "P4G.zip"

        file_path = download_dir / filename

        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Проверяем статус ответа

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        print(f"Размер файла: {total_size / 1024 / 1024:.2f} MB")
        print("Скачивание...")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Показываем прогресс если известен размер
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        sys.stdout.write(f"\rПрогресс: {percent:.1f}% ({downloaded/1024/1024:.2f}/{total_size/1024/1024:.2f} MB)")
                        sys.stdout.flush()
        
        if not file_path.exists():
            print("Руссификатор не установлен!")
            return None
        
        file_size = file_path.stat().st_size
        if file_size == 0:
            print("Руссификатор не установлен!")
            file_path.unlink()  # Удаляем пустой файл
            return None
            
        unzip_status = ArchiveZip(str(file_path), title) #Распаковка русификатора

        if settings.GetBackup() == False: 
            try:
                shutil.rmtree(settings.GetPath())
                        
            except Exception as e:
                os.rmdir(settings.GetPathStr())

            finally:
                print("Резервные копии удалены!")

        if unzip_status == False and settings.GetBackup() == False:
            print("Руссификатор не установлен! Попробуйте включить резервную копию для ручной установки!")
        else:
            print("Руссификатор установлен!")

    else:
        print("Игра не найдена!")
        
def ShowSettings():
    os.system('cls')

    settings.ShowInfo()

    print("\n0. Выйти из настроек")
    option = int(input("Выберите пункт, который вы хотите поменять -> "))

    if option == 1:
        lang = input("Делать резерную копию ? (Y/N)\n")
        settings.SetBackup(lang.lower())
    elif option == 2:
        pass #TODO

    else:
        pass

    os.system('cls')
        
"""Разорхивирует архив с руссификатором в файлы с игрой"""
def ArchiveZip(filename, game_title = ""):

    selected_folder = filedialog.askdirectory(title=f"Выберите папку с игрой:{game_title}")

    if not selected_folder:
        print("Папка не выбрана!")
        if settings.GetBackup() == True:
            subprocess.run(['explorer', filename])
        return False
    else:
        print("Идёт распаковка...")
        try:
            with ZipFile(filename, "r") as russ_zip:
                russ_zip.extractall(selected_folder)
                if settings.GetBackup() == True:
                    subprocess.run(['explorer', filename])
                else:
                    subprocess.run(['explorer', selected_folder])
                print("Распоковка завершена!")
                return True
        except Exception as e:
            print("Ошибка распаковки:", e)
            return False

if __name__ == "__main__":
    menu()