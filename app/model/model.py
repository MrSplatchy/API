import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import os

class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)  # (16, 32, 32)
        self.pool  = nn.MaxPool2d(2,2)               # (16, 16, 16)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1) # (32, 16, 16)
        self.fc1   = nn.Linear(32 * 8 * 8, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def classify_image(img):
    net = NeuralNet()
    
    # Chemin absolu ou relatif vers le fichier du modèle
    model_path = os.path.join(os.path.dirname(__file__), 'trained_net.pth')
    
    # Charger le modèle
    if os.path.exists(model_path):
        net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        print("Modèle chargé")
    else:
        raise FileNotFoundError(f"Le fichier de modèle n'a pas été trouvé : {model_path}")
    
    classes = ['avion', 'automobile', 'oiseau', 'chat', 'cerf', 'chien', 'grenouille', 'cheval', 'bateau', 'camion']
    
    # Assurez-vous que l'image est en mode RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Transformations de l'image
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    # Appliquer les transformations
    img_tensor = transform(img)
    
    # Ajouter une dimension pour le batch
    img_tensor = img_tensor.unsqueeze(0)
    
    # Passer en mode évaluation
    net.eval()
    
    with torch.no_grad():
        output = net(img_tensor)
        _, predicted = torch.max(output, 1)
    
    prediction = classes[predicted.item()]
    print(f"L'image est classifiée comme : {prediction}")
    
    return prediction