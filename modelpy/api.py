from PIL import Image
import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Определение модели
class PneumoniaNet(nn.Module):
    def __init__(self):
        super(PneumoniaNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(32 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, 2)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x


# Загрузка модели
model = PneumoniaNet()
model.load_state_dict(torch.load("pneumonia_mode312l.pth"))
model.eval()

# Трансформация для изображений
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ]
)

# Инициализация FastAPI
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:5500",
    "http://45.153.189.82:3001",
]

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
        # Чтение изображения из файла
        image = Image.open(file.file).convert("RGB")

        # Применение трансформаций
        image_tensor = transform(image).unsqueeze(0)  # Добавляем batch dimension

        # Предсказание
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs, 1)

        classes = ["Нет патологий", "Пневмония"]
        normal_prob = probabilities[0][0].item() * 100
        pneumonia_prob = probabilities[0][1].item() * 100

        result = {
            "predicted_class": classes[predicted.item()],
            "probability": {
                "Нет патологий": round(normal_prob, 2),
                "Пневмония": round(pneumonia_prob, 2),
            },
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9010)
