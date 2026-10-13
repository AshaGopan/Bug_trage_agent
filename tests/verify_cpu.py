import torch

print(f"PyTorch Version: {torch.__version__}")
print("CUDA Available (Should be False for this machine): " + str(torch.cuda.is_available()))
