from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import models, transforms
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

# === УСТРОЙСТВО ===
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === ЗАГРУЗКА МОДЕЛИ ===
model = models.densenet121(pretrained=False)
num_ftrs = model.classifier.in_features
model.classifier = torch.nn.Sequential(
    torch.nn.Linear(num_ftrs, 256),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.4),
    torch.nn.Linear(256, 2),
)
model.load_state_dict(
    torch.load("densenet121_pneumonia.pth", map_location=DEVICE)["model_state_dict"]
)
model.to(DEVICE)
model.eval()

# === ПРЕОБРАЗОВАНИЕ ИЗОБРАЖЕНИЯ ===
image_path = "chest_xray/test/PNEUMONIA/person1_virus_6.jpeg"
image = Image.open(image_path).convert("RGB")
original_image = image.resize((224, 224))

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)
input_tensor = transform(image).unsqueeze(0).to(DEVICE)

# === HOOK-и ===
gradients = None
activations = None


def save_gradient(grad):
    global gradients
    gradients = grad


def forward_hook(module, input, output):
    global activations
    activations = output
    output.register_hook(save_gradient)


target_layer = model.features.denseblock4
target_layer.register_forward_hook(forward_hook)

# === ПРОГОН ===
output = model(input_tensor)
class_idx = torch.argmax(output)
probs = F.softmax(output, dim=1)[0].cpu().detach().numpy()

# === ОБРАТНОЕ РАСПРОСТРАНЕНИЕ ===
model.zero_grad()
output[0, class_idx].backward()

# === ВЫЧИСЛЕНИЕ Grad-CAM ===
grads_val = gradients[0].cpu().detach().numpy()  # [C, H, W]
activations_val = activations[0].cpu().detach().numpy()  # [C, H, W]

weights = np.mean(grads_val, axis=(1, 2))
cam = np.zeros(activations_val.shape[1:], dtype=np.float32)
for i, w in enumerate(weights):
    cam += w * activations_val[i]

cam = np.maximum(cam, 0)
cam = cv2.resize(cam, (224, 224))
cam -= np.min(cam)
cam /= np.max(cam)
heatmap = (cam * 255).astype(np.uint8)
heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

# === НАЛОЖЕНИЕ ===
img_np = np.array(original_image)
superimposed_img = cv2.addWeighted(img_np, 0.6, heatmap_color, 0.4, 0)

# === ВИЗУАЛИЗАЦИЯ ===
classes = ["NORMAL", "PNEUMONIA"]
plt.figure(figsize=(10, 4))

plt.subplot(1, 3, 1)
plt.title("Original")
plt.imshow(img_np)
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Grad-CAM")
plt.imshow(superimposed_img)
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Heatmap Only")
plt.imshow(heatmap_color)
plt.axis("off")

plt.tight_layout()
plt.show()

# === ВЫВОД ===
print(f"Predicted class: {classes[class_idx]}")
print(f"Probability of NORMAL: {probs[0]*100:.2f}%")
print(f"Probability of PNEUMONIA: {probs[1]*100:.2f}%")

# === СОХРАНЕНИЕ ===
output_path = "gradcam_result.jpg"
cv2.imwrite(output_path, cv2.cvtColor(superimposed_img, cv2.COLOR_RGB2BGR))
print(f"Grad-CAM saved to: {os.path.abspath(output_path)}")
