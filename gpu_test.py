import torch

print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())
print("CUDA current device:", torch.cuda.current_device())
print(
    "Device name:",
    torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else "None",
)
