import gpiod
import gpiodevice

from datetime import timedelta
from rich.console import Console

from threading import Semaphore
from typing import Self

from pydantic import BaseModel, StrictInt, StrictStr, model_validator
from gpiod.line import Bias, Direction, Edge

from .utils import threaded


console = Console()


class ButtonMap(BaseModel):
    buttons: list[StrictInt] = [5, 6, 16, 24]
    labels: list[StrictStr] = ["A", "B", "C", "D"]

    @model_validator(mode="after")
    def validate_buttons_and_labels_lengths(self) -> Self:
        if len(self.buttons) != len(self.labels):
            raise ValueError("buttons and labels must have the same length")

        return self


class InkyButtons:
    def __init__(
        self,
        button_map: ButtonMap,
        debounce_period_ms: int = 100,
    ):
        self.button_map = button_map
        self.debounce_period_ms = debounce_period_ms

        self.semaphore = Semaphore(value=1)
        self.is_running: bool = False

    @threaded
    def start(self) -> None:
        self.semaphore.acquire()
        try:
            _input = gpiod.LineSettings(
                direction=Direction.INPUT,
                bias=Bias.PULL_UP,
                edge_detection=Edge.FALLING,
                debounce_period=timedelta(milliseconds=self.debounce_period_ms),
            )

            chip = gpiodevice.find_chip_by_platform()
            offsets = [
                chip.line_offset_from_id(pin) for pin in self.button_map.buttons
            ]

            request = chip.request_lines(
                consumer="inky-dsp-buttons",
                config=dict.fromkeys(offsets, _input),
            )

            self.is_running = True
            while self.is_running:
                for event in request.read_edge_events():
                    if not self.is_running:
                        break

                    index = offsets.index(event.line_offset)
                    button = self.button_map.labels[index]
                    gpio = self.button_map.buttons[index]
                    console.log(f"button {button} pressed on GPIO {gpio}")
        finally:
            self.semaphore.release()

    def stop(self) -> None:
        self.is_running = False
