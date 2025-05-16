from PIL import Image
import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F  # Для softmax


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

# Подготовка нового изображения
image_path = "chest_xray/test/PNEUMONIA/person1_virus_6.jpeg"
image = Image.open(image_path).convert("RGB")  # Преобразуем в RGB

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ]
)

image_tensor = transform(image).unsqueeze(0)  # Добавляем batch dimension

# Предсказание
with torch.no_grad():
    outputs = model(image_tensor)
    probabilities = F.softmax(outputs, dim=1)  # Применяем softmax
    _, predicted = torch.max(outputs, 1)
    classes = ["NORMAL", "PNEUMONIA"]

    # Получаем вероятности
    normal_prob = probabilities[0][0].item() * 100
    pneumonia_prob = probabilities[0][1].item() * 100

    print(f"Predicted class: {classes[predicted.item()]}")
    print(f"Probability of NORMAL: {normal_prob:.2f}%")
    print(f"Probability of PNEUMONIA: {pneumonia_prob:.2f}%")
