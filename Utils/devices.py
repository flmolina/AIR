import pyaudio

def mostrar_dispositivos():
    p = pyaudio.PyAudio()

    print("Dispositivos de entrada:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"ID: {i}, Nombre: {info['name']}")

    print("\nDispositivos de salida:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxOutputChannels'] > 0:
            print(f"ID: {i}, Nombre: {info['name']}")

    p.terminate()

if __name__ == "__main__":
    mostrar_dispositivos()
