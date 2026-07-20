class Actuator:
    def connect(self):
        raise NotImplementedError

    def move_absolute(self, position):
        raise NotImplementedError

    def get_position(self):
        raise NotImplementedError

    def wait_until_stopped(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError




def connect(self, serial_number: str) -> None:
        self._controller.Connect(serial_number)
        self._connected = True

    def get_position(self) -> float:
        self._require_connection()
        return float(self._controller.Position)

    def move_absolute(self, position: float) -> None:
        self._require_connection()
        self._controller.MoveTo(position)

    def move_relative(self, distance: float) -> None:
        self.move_absolute(self.get_position() + distance)

    def wait_until_stopped(self, timeout: float = 5.0) -> None:
        self._require_connection()

        # Replace this with the wrapper's real wait/polling method.
        success = self._controller.WaitForMotionComplete(
            int(timeout * 1000)
        )

        if not success:
            raise TimeoutError("Actuator did not stop before timeout.")

    def stop(self) -> None:
        if self._connected:
            self._controller.Stop()

    def close(self) -> None:
        if self._connected:
            self.stop()
            self._controller.Disconnect()
            self._connected = False

    def _require_connection(self) -> None:
        if not self._connected:
            raise RuntimeError("Actuator is not connected.")