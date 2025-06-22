import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
from tqdm import tqdm

# Параметры
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.0001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Пути к данным
DATA_DIR = "chest_xray"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
TEST_DIR = os.path.join(DATA_DIR, "test")

# Трансформации
data_transforms = {
    "train": transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    ),
    "val": transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    ),
}

# Загрузка данных
train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=data_transforms["train"])
val_dataset = datasets.ImageFolder(VAL_DIR, transform=data_transforms["val"])
test_dataset = datasets.ImageFolder(TEST_DIR, transform=data_transforms["val"])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Предобученная модель DenseNet121
model = models.densenet121(pretrained=True)
num_features = model.classifier.in_features
model.classifier = nn.Sequential(
    nn.Linear(num_features, 256), nn.ReLU(), nn.Dropout(0.4), nn.Linear(256, 2)
)
model = model.to(DEVICE)

# Функция потерь и оптимизатор
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)


# Обучение
def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        with tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}") as t:
            for inputs, labels in t:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                t.set_postfix(loss=loss.item())
        val_loss, val_acc = validate_model(model, val_loader, criterion)
        scheduler.step()
        print(f"Epoch {epoch+1}: Val Loss = {val_loss:.4f}, Val Acc = {val_acc:.4f}")


# Валидация
def validate_model(model, val_loader, criterion):
    model.eval()
    val_loss = 0.0
    correct = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
    val_loss /= len(val_loader)
    val_acc = correct / len(val_loader.dataset)
    return val_loss, val_acc


# Тестирование
def evaluate_on_test_set(model, test_loader, class_names):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    acc = accuracy_score(all_labels, all_preds) * 100
    print(f"\n📊 Точность на тесте: {acc:.2f}%")
    print(
        "Отчет классификации:\n",
        classification_report(all_labels, all_preds, target_names=class_names),
    )
    ConfusionMatrixDisplay.from_predictions(
        all_labels, all_preds, display_labels=class_names
    )
    plt.title("Матрица ошибок")
    plt.show()


# Запуск обучения
train_model(model, train_loader, val_loader, criterion, optimizer, EPOCHS)

# Сохранение модели
torch.save(
    {
        "model_state_dict": model.state_dict(),
        "class_to_idx": train_dataset.class_to_idx,
    },
    "densenet121_pneumonia.pth",
)

# Оценка на тесте
evaluate_on_test_set(model, test_loader, test_dataset.classes)
