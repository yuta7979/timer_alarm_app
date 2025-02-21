import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog
from PySide6.QtCore import QTimer
from timer import Timer

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Timer/Alarm App")
    self.setGeometry(100, 100, 400, 400)

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

    self.lap_button = QPushButton("Record Lap Time")
    self.lap_button.clicked.connect(self.record_lap)
    self.layout.addWidget(self.lap_button)

    self.lap_label = QLabel("Lap Times: ")
    self.layout.addWidget(self.lap_label)

    container = QWidget()
    container.setLayout(self.layout)
    self.setCentralWidget(container)

    self.timer_running = False
    self.lap_times = []
    self.current_time = 0

  def start_timer(self):
    if self.timer_running:
      return

    duration, ok = QInputDialog.getInt(
        self, "Input", "Enter duration in seconds:")
    if ok:
      self.timer.start(duration)
      self.timer_running = True
      self.update_timer_ui(duration)

  def update_timer_ui(self, seconds):
    self.label.setText(f"Timer: {seconds} seconds remaining")
    self.current_time = seconds

    if seconds > 0:
      QTimer.singleShot(1000, lambda: self.update_timer_ui(seconds - 1))

  def stop_timer(self):
    self.timer.stop()
    self.timer_running = False
    self.label.setText("Timer stopped")

  def on_timer_finished(self):
    self.label.setText("Timer finished!")
    print("\a")

  def record_lap(self):
    if self.timer_running:
      self.lap_times.append(self.current_time)
      lap_time_text = " | ".join([f"{lap} sec" for lap in self.lap_times])
      self.lap_label.setText(f"Lap Times: {lap_time_text}")
    else:
      self.lap_label.setText("Lap Times: Timer not running")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
