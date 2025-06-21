import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 1. Define the CheXNet model
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


# 2. Load the model and checkpoint
model = CheXNet()
checkpoint = torch.load("chexnet.pth.tar", map_location=DEVICE)

# Fix for "module." prefix in state_dict keys (if present)
new_state_dict = {
    k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()
}
model.load_state_dict(new_state_dict, strict=False)

# Move model to device and set to evaluation mode
model = model.to(DEVICE)
model.eval()

# 3. Define CheXNet classes
CHEXNET_CLASSES = [
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

# 4. Define image transformation
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

# 5. Load and preprocess the image
img_path = "norm.jpeg"  # Replace with your image path
img = Image.open(img_path).convert("RGB")
input_tensor = transform(img).unsqueeze(0).to(DEVICE)

# 6. Make predictions
with torch.no_grad():
    output = model(input_tensor)
    probs = torch.sigmoid(output).cpu().numpy()[0]

print("Predicted probabilities:")
for i, prob in enumerate(probs):
    print(f"{CHEXNET_CLASSES[i]}: {prob:.4f}")


# 7. Grad-CAM implementation
def generate_gradcam(model, image_tensor, class_index, target_layer):
    model.eval()
    gradients = []
    activations = []

    def save_gradient(grad):
        gradients.append(grad)

    def forward_hook(module, input, output):
        activations.append(output)
        output.register_hook(save_gradient)

    # Register hooks
    handle = target_layer.register_forward_hook(forward_hook)

    # Forward pass
    output = model(image_tensor)
    model.zero_grad()

    # Backward pass for the target class
    class_loss = output[0, class_index]
    class_loss.backward()

    # Extract gradients and activations
    grad = gradients[0][0].cpu().data.numpy()
    act = activations[0][0].cpu().data.numpy()

    # Compute weights and Grad-CAM
    weights = np.mean(grad, axis=(1, 2))
    cam = np.zeros(act.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * act[i]

    cam = np.maximum(cam, 0)  # Apply ReLU
    cam = cv2.resize(cam, (224, 224))  # Resize to match input image size
    cam = cam - cam.min()
    cam = cam / cam.max()  # Normalize between 0 and 1

    handle.remove()
    return cam


# 8. Visualize Grad-CAM
target_class_index = 3  # Example: Infiltration
target_layer = model.densenet.features[-1]  # Last convolutional layer
cam = generate_gradcam(model, input_tensor, target_class_index, target_layer)

# Overlay Grad-CAM heatmap on the original image
img_np = np.array(img.resize((224, 224))) / 255.0
heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
heatmap = np.float32(heatmap) / 255
overlay = heatmap + img_np
overlay = overlay / overlay.max()

# Plot results
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(img_np)

plt.subplot(1, 2, 2)
plt.title(f"Grad-CAM: {CHEXNET_CLASSES[target_class_index]}")
plt.imshow(overlay)
plt.show()
