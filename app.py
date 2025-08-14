import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, 
    QVBoxLayout, QCheckBox, QPushButton, 
    QComboBox, QLabel
)
from PyQt6.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки системы")
        self.setGeometry(100, 100, 300, 200)
        
        # Стилизация окна
        self.setStyleSheet(
            """
            QDialog {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                color: #ECEFF4;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #ECEFF4;
                padding: 5px 0;
            }
            QComboBox, QCheckBox {
                background-color: #4C566A;
                border: 1px solid #5E81AC;
                border-radius: 4px;
                padding: 4px;
                color: #ECEFF4;
            }
            QComboBox::drop-down {
                background-color: #5E81AC;
                border-left: 1px solid #4C566A;
            }
            QPushButton {
                background-color: #8FBCBB;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: #2E3440;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            """
        )
        
        layout = QVBoxLayout()
        
        # Элементы настроек
        self.logging_checkbox = QCheckBox("Включить детальное логирование")
        self.logging_checkbox.setChecked(True)
        layout.addWidget(self.logging_checkbox)
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["720p", "1080p", "4K"])
        layout.addWidget(QLabel("Разрешение видеопотока:"))
        layout.addWidget(self.resolution_combo)
        
        self.save_btn = QPushButton("Сохранить настройки")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("proba.ui", self)
        self.setWindowTitle("Система мониторинга объектов")
        
        # Начальное состояние
        self.stop.setEnabled(False)
        
        # Подключаем обработчики
        self.play.clicked.connect(self.start_video)
        self.stop.clicked.connect(self.stop_video)
        self.settings.clicked.connect(self.open_settings)

    def start_video(self):
        self.videoLayout.setText("Видеопоток активен")
        self.log_event("Видеопоток запущен", "INFO")
        self.stop.setEnabled(True)
        self.play.setEnabled(False)

    def stop_video(self):
        self.videoLayout.setText("Видеопоток отключен")
        self.log_event("Видеопоток остановлен", "WARNING")
        self.play.setEnabled(True)
        self.stop.setEnabled(False)

    def open_settings(self):
        """Обработчик кнопки настроек"""
        # Устанавливаем сообщение в статус-бар
        self.statusBar().showMessage("Меню настроек открыто")
        
        # Открываем окно настроек
        settings_dialog = SettingsWindow(self)
        if settings_dialog.exec():
            # Обработка сохраненных настроек
            resolution = settings_dialog.resolution_combo.currentText()
            logging_enabled = settings_dialog.logging_checkbox.isChecked()
            
            self.log_event(f"Изменены настройки: разрешение={resolution}, логирование={logging_enabled}", "INFO")
        else:
            self.log_event("Настройки отменены", "INFO")
        
        # Сбрасываем сообщение в статус-бар
        self.statusBar().showMessage("")

    def log_event(self, message, level):
        color = "#88C0D0" if level == "INFO" else "#EBCB8B"
        self.textBrowser.append(f'<span style="color: {color};">[{level}] {message}</span>')
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())