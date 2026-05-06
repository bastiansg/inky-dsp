import gpiod
import gpiodevice

from datetime import timedelta
from threading import Lock
from rich.console import Console
from typing import Awaitable, Callable, Self

from pydantic import BaseModel, StrictInt, StrictStr, model_validator
from gpiod.line import Bias, Direction, Edge


console = Console()


class ButtonMap(BaseModel):
    buttons: list[StrictInt] = [5, 6, 16, 24]
    labels: list[StrictStr] = ["A", "B", "C", "D"]

    @model_validator(mode="after")
    def validate_buttons_and_labels_lengths(self) -> Self:
        if len(self.buttons) != len(self.labels):
            raise ValueError("buttons and labels must have the same length")

        return self


class ButtonEvent(BaseModel):
    label: StrictStr
    gpio: StrictInt
    index: StrictInt


class InkyButtons:
    def __init__(
        self,
        button_map: ButtonMap,
        callback: Callable[[ButtonEvent], Awaitable[None]],
        debounce_period_ms: int = 100,
    ):
        self.button_map = button_map
        self.callback = callback
        self.debounce_period_ms = debounce_period_ms

        self.start_lock = Lock()
        self.is_running: bool = False

    # @threaded
    async def run(self) -> None:
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

        while True:
            for event in request.read_edge_events():
                index = offsets.index(event.line_offset)
                await self.callback(
                    ButtonEvent(
                        label=self.button_map.labels[index],
                        gpio=self.button_map.buttons[index],
                        index=index,
                    )
                )

                while request.wait_edge_events(timeout=timedelta()):
                    request.read_edge_events()
