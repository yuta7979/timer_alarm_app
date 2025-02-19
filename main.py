import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog
from PySide6.QtCore import QTimer
from timer import Timer

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Timer/Alarm App")
    self.setGeometry(100, 100, 400, 300)

    self.timer = Timer()
    self.timer.timer_finished.connect(self.on_timer_finished)

    self.layout = QVBoxLayout()

    self.label = QLabel("Timer: 00:00")
    self.layout.addWidget(self.label)

    self.start_button = QPushButton("Start Timer")
    self.start_button.clicked.connect(self.start_timer)
    self.layout.addWidget(self.start_button)

    self.stop_button = QPushButton("Stop Timer")
    self.stop_button.clicked.connect(self.stop_timer)
    self.layout.addWidget(self.stop_button)

    container = QWidget()
    container.setLayout(self.layout)
    self.setCentralWidget(container)

  def start_timer(self):
    duration, ok = QInputDialog.getInt(
        self, "Input", "Enter duration in seconds:")
    if ok:
      self.timer.start(duration)
      self.update_timer_ui(duration)

  def update_timer_ui(self, seconds):
    self.label.setText(f"Timer: {seconds} seconds remaining")
    if seconds > 0:
      QTimer.singleShot(1000, lambda: self.update_timer_ui(seconds - 1))

  def stop_timer(self):
    self.timer.stop()
    self.label.setText("Timer stopped")

  def on_timer_finished(self):
    self.label.setText("Timer finished!")
    print("\a")  # This will trigger a beep sound

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
