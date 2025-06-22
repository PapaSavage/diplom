from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
import cv2
import io
import base64
import matplotlib.pyplot as plt
import uvicorn

# Настройка устройства
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Классы CheXNet
CHEXNET_CLASSES = [
    "Ателектаз",
    "Кардиомегалия",
    "Эффузия",
    "Инфильтрация",
    "Образование",
    "Узел",
    "Пневмония",
    "Пневмоторакс",
    "Консолидация",
    "Отёк",
    "Эмфизема",
    "Фиброз",
    "Утолщение плевры",
    "Грыжа",
]

CLASS_TRANSLATIONS = {
    "Atelectasis": "Ателектаз",
    "Cardiomegaly": "Кардиомегалия",
    "Effusion": "Эффузия",
    "Infiltration": "Инфильтрация",
    "Mass": "Образование",
    "Nodule": "Узел",
    "Pneumonia": "Пневмония",
    "Pneumothorax": "Пневмоторакс",
    "Consolidation": "Консолидация",
    "Edema": "Отёк",
    "Emphysema": "Эмфизема",
    "Fibrosis": "Фиброз",
    "Pleural_Thickening": "Утолщение плевры",
    "Hernia": "Грыжа",
}


# Трансформация изображений
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


# Определение модели
class CheXNet(nn.Module):
    def __init__(self, num_classes=14):
        super(CheXNet, self).__init__()
        self.densenet = models.densenet121(
            weights=models.DenseNet121_Weights.IMAGENET1K_V1
        )
        num_ftrs = self.densenet.classifier.in_features
        self.densenet.classifier = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        return self.densenet(x)


# Загрузка модели
model = CheXNet()
checkpoint = torch.load("chexnet.pth.tar", map_location=DEVICE)
new_state_dict = {
    k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()
}
model.load_state_dict(new_state_dict, strict=False)
model.to(DEVICE)
model.eval()


# Grad-CAM генерация
def generate_gradcam(model, image_tensor, class_index, target_layer):
    model.eval()
    gradients = []
    activations = []

    def save_gradient(grad):
        gradients.append(grad)

    def forward_hook(module, input, output):
        activations.append(output)
        output.register_hook(save_gradient)

    handle = target_layer.register_forward_hook(forward_hook)
    output = model(image_tensor)
    model.zero_grad()

    class_loss = output[0, class_index]
    class_loss.backward()

    grad = gradients[0][0].cpu().data.numpy()
    act = activations[0][0].cpu().data.numpy()
    weights = np.mean(grad, axis=(1, 2))
    cam = np.zeros(act.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * act[i]

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam -= cam.min()
    cam /= cam.max()
    handle.remove()
    return cam


# Конвертация Grad-CAM в base64
def cam_to_base64(original_image, cam):
    cam = cv2.GaussianBlur(cam, (7, 7), 0)
    cam = np.maximum(cam - 0.3, 0)  # подавление слабых сигналов

    img_np = np.array(original_image) / 255.0  # оригинальное изображение
    cam_resized = cv2.resize(cam, (img_np.shape[1], img_np.shape[0]))  # на весь размер

    heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
    heatmap = np.float32(heatmap) / 255
    overlay = heatmap + img_np
    overlay = overlay / np.max(overlay)

    overlay = np.uint8(255 * overlay)
    _, buffer = cv2.imencode(".png", overlay)
    img_base64 = base64.b64encode(buffer).decode("utf-8")
    return img_base64


# Инициализация FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/diagnosis")
async def diagnosis(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            output = model(image_tensor)
            probs = torch.sigmoid(output).cpu().numpy()[0]

        # Вероятности в виде "патология: %"
        predictions = {
            CHEXNET_CLASSES[i]: round(float(prob) * 100, 2)
            for i, prob in enumerate(probs)
        }

        # Топ патология
        top_index = int(np.argmax(probs))
        top_class = CHEXNET_CLASSES[top_index]

        # Grad-CAM
        target_layer = model.densenet.features[-1]
        cam = generate_gradcam(model, image_tensor, top_index, target_layer)
        cam_base64 = cam_to_base64(image, cam)

        return {
            "top_class": top_class,
            "probabilities": predictions,
            "gradcam": cam_base64,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9010)
