import torch
import threading
import torchaudio

import numpy as np
import sounddevice as sd
import torchaudio.functional as F


class AudioRecorder:
    def __init__(
        self,
        record_sample_rate: int = 48000,
        out_sample_rate: int = 16000,
        channels: int = 1,
        sd_sleep: int = 100,
        out_path: str = "/resources/audios/recorded-audio.wav",
    ):
        self.sd_sleep = sd_sleep
        self.channels = channels
        self.record_sample_rate = record_sample_rate
        self.out_sample_rate = out_sample_rate
        self.out_path = out_path

        self.recording = False
        self.audio_data = []

    def _record_callback(
        self,
        audio_frames: np.ndarray,
        *args,
        **kwargs,
    ) -> None:
        if self.recording:
            self.audio_data.append(audio_frames.copy())

    def _record(self) -> None:
        with sd.InputStream(
            callback=self._record_callback,
            samplerate=self.record_sample_rate,
            channels=self.channels,
        ):
            while self.recording:
                sd.sleep(self.sd_sleep)

    def start_record(self) -> None:
        self.recording = True
        threading.Thread(target=self._record).start()

    def stop_record(self) -> None:
        self.recording = False
        audio_data = np.concatenate(self.audio_data, axis=0)
        audio_tensor = torch.from_numpy(audio_data.T)
        resampled_waveform = F.resample(
            waveform=audio_tensor,
            orig_freq=self.record_sample_rate,
            new_freq=self.out_sample_rate,
        )

        torchaudio.save(
            uri=self.out_path,
            src=resampled_waveform,
            sample_rate=self.out_sample_rate,
        )

        self.audio_data = []
