from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import models, transforms
import numpy as np
import cv2
import io
import base64
import uvicorn

# Настройка устройства
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Классы для модели
CLASSES = ["Норма", "Пневмония"]

# Трансформация изображений
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

# Загрузка модели
model = models.densenet121(pretrained=False)
num_ftrs = model.classifier.in_features
model.classifier = torch.nn.Sequential(
    torch.nn.Linear(num_ftrs, 256),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.4),
    torch.nn.Linear(256, 2),
)
checkpoint = torch.load("densenet121_pneumonia.pth", map_location=DEVICE)
model.load_state_dict(checkpoint["model_state_dict"])
model.to(DEVICE)
model.eval()


# Генерация Grad-CAM
def generate_gradcam(model, image_tensor, class_idx, target_layer):
    gradients = None
    activations = None

    def save_gradient(grad):
        nonlocal gradients
        gradients = grad

    def forward_hook(module, input, output):
        nonlocal activations
        activations = output
        output.register_hook(save_gradient)

    # Регистрация хука на целевом слое
    handle = target_layer.register_forward_hook(forward_hook)

    # Прямой проход через модель
    output = model(image_tensor)
    model.zero_grad()

    # Вычисление градиента для целевого класса
    class_loss = output[0, class_idx]
    class_loss.backward()

    # Получение градиентов и активаций
    grads_val = gradients[0].cpu().detach().numpy()  # [C, H, W]
    activations_val = activations[0].cpu().detach().numpy()  # [C, H, W]

    # Веса для Grad-CAM
    weights = np.mean(grads_val, axis=(1, 2))
    cam = np.zeros(activations_val.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * activations_val[i]

    # Постобработка карты активации
    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam -= np.min(cam)
    cam /= np.max(cam)

    handle.remove()
    return cam


# Конвертация Grad-CAM в base64
def cam_to_base64(original_image, cam):
    # Преобразуем исходное изображение в массив NumPy
    img_np = np.array(original_image)  # [H, W, 3], значения в диапазоне [0, 255]

    # Масштабируем Grad-CAM до размера исходного изображения
    cam_resized = cv2.resize(cam, (img_np.shape[1], img_np.shape[0]))  # [H, W]

    # Применяем цветовую палитру JET к тепловой карте
    heatmap = cv2.applyColorMap(
        np.uint8(255 * cam_resized), cv2.COLORMAP_JET
    )  # [H, W, 3], значения в диапазоне [0, 255]

    # Нормализуем тепловую карту для наложения
    heatmap = heatmap.astype(np.float32) / 255.0  # Приводим к диапазону [0, 1]

    # Нормализуем исходное изображение для наложения
    img_np = img_np.astype(np.float32) / 255.0  # Приводим к диапазону [0, 1]

    # Накладываем тепловую карту на исходное изображение
    overlay = cv2.addWeighted(img_np, 0.6, heatmap, 0.4, 0)

    # Конвертируем результат обратно в uint8 для сохранения
    overlay = np.uint8(255 * overlay)

    # Кодируем изображение в base64
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
        # Загрузка изображения
        image = Image.open(file.file).convert("RGB")
        original_image = image.copy()
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # Предсказание модели
        with torch.no_grad():
            output = model(image_tensor)
            probs = F.softmax(output, dim=1).cpu().numpy()[0]

        # Вероятности в виде "класс: %"
        predictions = {
            CLASSES[i]: round(float(prob) * 100, 2) for i, prob in enumerate(probs)
        }

        # Топ класс
        top_index = int(np.argmax(probs))
        top_class = CLASSES[top_index]

        # Grad-CAM
        target_layer = model.features.denseblock4
        cam = generate_gradcam(model, image_tensor, top_index, target_layer)
        cam_base64 = cam_to_base64(original_image, cam)

        return {
            "top_class": top_class,
            "probabilities": predictions,
            "gradcam": cam_base64,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9010)
