import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models

# Load your model
model = models.densenet201(weights=None)
model.load_state_dict(torch.load("densenet201.pth"))
model.eval()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

classes = ["NORMAL", "DRUSEN", "CNV", "DME"]

def classify(image_path):
    im = Image.open(image_path).convert("RGB")
    im = preprocess(im).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(im)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)

    predicted_class_name = classes[predicted_class.item()]
    return predicted_class_name, confidence.item()