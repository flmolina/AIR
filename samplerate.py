import pyaudio

p = pyaudio.PyAudio()
info = p.get_device_info_by_index(11)  # Reemplaza con el índice de tu dispositivo

print(info)
