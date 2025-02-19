import time
import threading
from PySide6.QtCore import QObject, Signal

class Timer(QObject):
  timer_finished = Signal()

  def __init__(self):
    super().__init__()
    self._timer_thread = None
    self._running = False

  def start(self, duration):
    self._running = True
    self._timer_thread = threading.Thread(
        target=self._countdown, args=(duration,))
    self._timer_thread.start()

  def stop(self):
    self._running = False
    if self._timer_thread is not None:
      self._timer_thread.join()

  def _countdown(self, duration):
    while duration > 0 and self._running:
      time.sleep(1)
      duration -= 1

    if self._running:
      self.timer_finished.emit()
