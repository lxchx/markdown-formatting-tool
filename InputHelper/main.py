from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from MainTool import MainTool

def main():
    app = QGuiApplication([])
    engine = QQmlApplicationEngine()

    tool = MainTool()
    engine.rootContext().setContextProperty("tool",tool)

    engine.load(r'QML\main.qml')
    app.exec_()
        
    

if __name__ == '__main__':
    main()