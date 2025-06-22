# predict_one.py
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os

# ==== Константы ====
IMAGE_PATH = "chest_xray/test/PNEUMONIA/person1_virus_6.jpeg"  # Путь до изображения
CHECKPOINT_PATH = "chexnet.pth.tar"  # Файл с весами
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = [
    "Atelectasis",
    "Cardiomegaly",
    "Effusion",
    "Infiltration",
    "Mass",
    "Nodule",
    "Pneumonia",
    "Pneumothorax",
    "Consolidation",
    "Edema",
    "Emphysema",
    "Fibrosis",
    "Pleural_Thickening",
    "Hernia",
]


# ==== Модель ====
class DenseNet121(nn.Module):
    def __init__(self, out_size):
        super(DenseNet121, self).__init__()
        self.densenet121 = models.densenet121(pretrained=True)
        num_ftrs = self.densenet121.classifier.in_features
        self.densenet121.classifier = nn.Sequential(
            nn.Linear(num_ftrs, out_size), nn.Sigmoid()
        )

    def forward(self, x):
        return self.densenet121(x)


# ==== Загрузка модели ====
model = DenseNet121(len(CLASS_NAMES)).to(DEVICE)
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
state_dict = {k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()}
model.load_state_dict(state_dict)
model.eval()

# ==== Преобразования ====
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


# ==== Grad-CAM ====
def generate_gradcam(image_tensor, model, class_index):
    gradients = []
    activations = []

    def save_gradient(grad):
        gradients.append(grad)

    def forward_hook(module, input, output):
        activations.append(output)
        output.register_hook(save_gradient)

    handle = model.densenet121.features[-1].register_forward_hook(forward_hook)

    output = model(image_tensor)
    model.zero_grad()
    loss = output[0, class_index]
    loss.backward()

    grads_val = gradients[0][0].cpu().data.numpy()
    fmap = activations[0][0].cpu().data.numpy()

    weights = np.mean(grads_val, axis=(1, 2))
    cam = np.zeros(fmap.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * fmap[i]
    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam -= cam.min()
    cam /= cam.max()

    handle.remove()
    return cam


# ==== Предсказание ====
image = Image.open(IMAGE_PATH).convert("RGB")
image_tensor = transform(image).unsqueeze(0).to(DEVICE)

with torch.no_grad():
    output = model(image_tensor)
    probs = output.cpu().numpy()[0]

# ==== Вывод вероятностей ====
for i, prob in enumerate(probs):
    print(f"{CLASS_NAMES[i]}: {prob:.3f}")

top_idx = int(np.argmax(probs))
print(f"\nTop pathology: {CLASS_NAMES[top_idx]} ({probs[top_idx]:.3f})")

# ==== Grad-CAM визуализация ====
cam = generate_gradcam(image_tensor, model, top_idx)

# Наложение heatmap
img_np = np.array(image.resize((224, 224))) / 255.0
heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
heatmap = np.float32(heatmap) / 255
overlay = heatmap + img_np
overlay = overlay / np.max(overlay)

# ==== Отображение ====
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image.resize((224, 224)))
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title(f"Grad-CAM: {CLASS_NAMES[top_idx]}")
plt.imshow(np.uint8(255 * overlay))
plt.axis("off")

plt.tight_layout()
plt.show()
