import glob
import random

import torch
import torchaudio
from torch.utils.data import Dataset


class NSynthDataset(Dataset):
    """Dataset to load NSynth data."""
    
    def __init__(self, audio_dir):
        super().__init__()

        self.filenames = glob.glob(audio_dir + "/**/*.wav", recursive=True)
        _, self.sr = torchaudio.load(self.filenames[0])
    
    def __len__(self):
        return len(self.filenames)
    
    def __getitem__(self, index):
        wave, sr = torchaudio.load(self.filenames[index])
        if sr != 8000:
            wave = torchaudio.functional.resample(wave, orig_freq=sr, new_freq=8000)
        sr = 8000
        len_wav = len(wave[0])
        if len_wav < sr * 2:
            wave = torch.nn.functional.pad(wave, (0, sr * 2 + 1 - len_wav), "constant", 0)
        len_wav = len(wave[0])
        begin = random.randint(0, len_wav - sr * 2)
        wave = wave[:, begin:begin + sr * 2]
        return wave
