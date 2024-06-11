import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import matplotlib.pyplot as plt
import numpy as np

# Load your model
print("Loading model...")
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

def generate_grad_cam(model, image_tensor, target_layer):
    print("Generating Grad-CAM...")
    gradients = []
    activations = []

    def forward_hook(module, input, output):
        activations.append(output)

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    handle_forward = target_layer.register_forward_hook(forward_hook)
    handle_backward = target_layer.register_backward_hook(backward_hook)

    model.zero_grad()
    output = model(image_tensor)
    class_idx = torch.argmax(output, dim=1).item()
    output[0, class_idx].backward()

    handle_forward.remove()
    handle_backward.remove()

    gradient = gradients[0].cpu().data.numpy()[0]
    activation = activations[0].cpu().data.numpy()[0]

    weights = np.mean(gradient, axis=(1, 2))
    cam = np.zeros(activation.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * activation[i]

    cam = np.maximum(cam, 0)
    cam = cam - np.min(cam)
    cam = cam / np.max(cam)
    cam = np.uint8(cam * 255)

    return cam

def save_grad_cam(image_path, cam, output_path):
    print("Saving Grad-CAM image...")
    image = Image.open(image_path).convert("RGB")
    image = np.array(image)
    height, width, _ = image.shape
    cam = Image.fromarray(cam).resize((width, height), Image.BILINEAR)
    cam = np.array(cam)

    heatmap = plt.get_cmap("jet")(cam / 255.0)[:, :, :3]
    heatmap = np.uint8(heatmap * 255)
    overlay = heatmap * 0.6 + image * 0.4  # Adjusted overlay intensity
    overlay = np.uint8(overlay)

    Image.fromarray(overlay).save(output_path)
    print(f"Grad-CAM image saved to {output_path}")

def classify(image_path):
    print(f"Classifying image: {image_path}")
    im = Image.open(image_path).convert("RGB")
    im = preprocess(im).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(im)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)

    predicted_class_name = classes[predicted_class.item()]

    # Generate Grad-CAM
    target_layer = model.features[-1]
    cam = generate_grad_cam(model, im, target_layer)
    cam_output_path = image_path.replace(".jpg", "_cam.jpg")
    save_grad_cam(image_path, cam, cam_output_path)

    print(f"Prediction: {predicted_class_name}, Confidence: {confidence.item()}, CAM Image: {cam_output_path}")
    return predicted_class_name, confidence.item(), cam_output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        classify(sys.argv[1])
    else:
        print("Please provide an image file path as an argument.")
