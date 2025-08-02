import platform
import psutil
import GPUtil

def benchmark_system():
    print("🖥 CPU:", platform.processor())
    print("💾 RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

    gpus = GPUtil.getGPUs()
    print(gpus)
    for gpu in gpus:
        print(f"\n🖼 GPU Name: {gpu.name}")
        print(f"📦 Total Memory: {round(gpu.memoryTotal / 1024, 2)} GB")
        print(f"📈 Used Memory: {round(gpu.memoryUsed / 1024, 2)} GB")
        print(f"🔧 Driver Version: {gpu.driver}")
        print(f"🧬 UUID: {gpu.uuid}")

benchmark_system()
