# -*- coding: utf-8 -*-
from typing import Any, List
import numpy as np
import dawdreamer
import librosa
from pathlib import Path
from scipy.io import wavfile

p: str = str((Path(__file__).parent.parent / "install_TAL-Chorus-LX" / "TAL-Chorus-LX.vst3" / "Contents" / "x86_64-win" / "TAL-Chorus-LX.vst3").as_posix())

SAMPLE_RATE = 44100
BUFFER_SIZE = 512

print(p)

def main():
  engine = dawdreamer.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
  guitar_audio, _ = librosa.load("GTR.wav", sr=SAMPLE_RATE, mono=True)
  guitar = engine.make_playback_processor("guitar", guitar_audio.reshape(1, -1)) # reshape for mono track
  try:
      plugin = engine.make_plugin_processor("test", p)
      plugin.load_state('test-state-1')
      plugin.open_editor()
      plugin.save_state('test-state-1')

      print(f"✔️ Plugin loaded successfully")
      print(f"Inputs: {plugin.get_num_input_channels()}")
      print(f"Outputs: {plugin.get_num_output_channels()}")

      engine.load_graph([
         
         (plugin, ["guitar"])])
      engine.render(5.0)
      audio = engine.get_audio()
  
      # Check for NaN
      if np.isnan(audio).any():
          print("❌ Output contains NaN values")
      else:
          wavfile.write('final_mix.wav', SAMPLE_RATE, audio.transpose())
          print("✔️ Rendering successful")
  
  except Exception as e:
      print(f"❌ Error: {e}")

if __name__ == "__main__":
  main()



