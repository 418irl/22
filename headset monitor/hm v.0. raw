import time
import threading
from datetime import datetime
from plyer import notification
import matplotlib.pyplot as plt
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import IAudioEndpointVolume
from pycaw.utils import AudioUtilities as AU
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.constants import PKEY_Device_FriendlyName


def is_headset_connected():
    devices = AudioUtilities.GetSpeakers()
    properties = devices.OpenPropertyStore(0)  # 0 = STGM_READ
    name = properties.GetValue(PKEY_Device_FriendlyName).value
    print(f"Current audio output device: {name}")
    return HEADSET_NAME.lower() in name.lower()


# ====== CONFIG ======
HEADSET_NAME = "Beats Studio 3"  
VOLUME_THRESHOLD = 0.8  # 80%
HIGH_VOLUME_DURATION_LIMIT = 120  # 2 minutes
CHECK_INTERVAL = 5  # seconds
TIMER_DURATION = 1800  # 30 minutes in seconds
# =====================

volume_data = []
timestamps = []
high_volume_start = None
stop_volume_monitor = False
device_connected = False


def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )


def get_system_volume():
    devices = AU.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def volume_monitor():
    global high_volume_start
    while not stop_volume_monitor:
        vol = get_system_volume()
        current_time = time.time()
        volume_data.append(vol)
        timestamps.append(current_time)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Volume: {vol:.2f}")

        if vol > VOLUME_THRESHOLD:
            if high_volume_start is None:
                high_volume_start = current_time
            elif current_time - high_volume_start > HIGH_VOLUME_DURATION_LIMIT:
                notify("Volume Alert", "Volume has been high for over 2 mins!")
                high_volume_start = None
        else:
            high_volume_start = None

        time.sleep(CHECK_INTERVAL)


def timer_30_min():
    time.sleep(TIMER_DURATION)
    notify("Time Up", "You've been using your headphones for 30 minutes!")


def plot_volume():
    if not volume_data:
        print("No volume data to plot.")
        return
    relative_time = [t - timestamps[0] for t in timestamps]
    plt.plot(relative_time, volume_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Volume Level")
    plt.title("Volume Over Time")
    plt.grid(True)
    plt.show()


def main():
    global stop_volume_monitor, device_connected

    print("Monitoring headset connection...")

    while True:
        connected = is_headset_connected()
        if connected and not device_connected:
            notify("Headset Connected", f"{HEADSET_NAME} is now connected.")
            print("Headset connected! Starting monitoring...")

            device_connected = True
            start_time = time.time()

            vol_thread = threading.Thread(target=volume_monitor)
            vol_thread.start()

            timer_thread = threading.Thread(target=timer_30_min)
            timer_thread.start()

        elif not connected and device_connected:
            stop_volume_monitor = True
            device_connected = False
            end_time = time.time()
            total_time = end_time - start_time
            notify("Headset Disconnected", f"Used for {int(total_time)} seconds.")
            print("Headset disconnected. Plotting data...")
            plot_volume()
            break

        time.sleep(3)


if __name__ == "__main__":
    main()
