from PyQt5.QtCore import pyqtProperty, pyqtSlot, QObject, Qt, QAbstractListModel
from PyQt5.QtQml import qmlRegisterType

from win32 import win32api, win32gui
from win32.lib import win32con

import yaml

import pyautogui

import pyperclip

import os

from Utils import FocusSetter, InputUtils, ListModel

from Utils.ListModel import ListModel
from Utils.WindowEffect import WindowEffect

class MainTool(QObject):
    def __init__(self, *args, **kwargs):
        super(MainTool, self).__init__(*args, **kwargs)
        self.winEffect = WindowEffect()
        self._model = ListModel()

    @pyqtSlot()
    def load_model(self):
        mod = self._model

        # 添加roleName
        role_names = ['display_text', 'description', 'operation']
        for i in range(len(role_names)):
            mod.addRoleName(Qt.UserRole + 1 + i, role_names[i])

        # 从data.yaml导入模型
        file_name = r'.\Config\data.yaml'
        with open(file_name, 'rb') as f:
            data = yaml.safe_load(f)
        print(data)

        data = data['data']
        mod.setItems(data)

    @pyqtSlot()
    def edit(self):
        os.system("start "+ r'Config\data.yaml') 


    @pyqtSlot(str)
    def oparate(self, opa: str):
        last_clip = pyperclip.paste()

        pyautogui.hotkey('ctrl', 'c')  #模拟复制热键
        selected = pyperclip.paste()

        if selected == last_clip: selected = ''  # 选空或复制失败就将$设为空
        
        position = len(opa) - opa.find('$')

        result = opa.replace('$', selected)
        pyperclip.copy(result)
        pyautogui.hotkey('ctrl', 'v')  #模拟粘贴热键

        for i in range(position-1): pyautogui.press('left')  #将光标移到$位置

        pyperclip.copy(last_clip)


    @pyqtProperty(ListModel)
    def model(self) -> ListModel:
        return self._model

    @pyqtSlot(QObject)
    def move_window(self, qObj):
        hWnd = qObj.winId()
        win32gui.ReleaseCapture()
        win32api.SendMessage(hWnd, win32con.WM_SYSCOMMAND,
                             win32con.SC_MOVE + win32con.HTCAPTION, 0)

    @pyqtSlot(QObject)
    def setAeroEffect(self, qObj):
        hWnd = qObj.winId()
        self.winEffect.setAeroEffect(hWnd)

    @pyqtSlot(QObject)
    def set_no_focus(self, qObj):
        hWnd = qObj.winId()
        FocusSetter.set_no_focus(int(hWnd))