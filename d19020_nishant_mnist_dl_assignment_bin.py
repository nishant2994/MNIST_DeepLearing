# -*- coding: utf-8 -*-
"""D19020_Nishant_MNIST_DL_assignment.bin

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1scYuNzYeHAbhboMZY3ORNQK9tvIqM1WO
"""

#Importing Packages
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import nn,optim
import torchvision.transforms as transforms
import torchvision.datasets as dsets
from torchvision import models
from torchsummary import summary

'''
STEP 1: LOADING the DATASET
'''
train_dataset = dsets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=True)
test_dataset = dsets.MNIST(root='./data', train=False, transform=transforms.ToTensor())

'''
STEP 2: MAKING DATASET ITERABLE
'''
#Creating a batch size.
batch_size = 200
#Initilizing number of Epochs
num_epochs = 10
n_iters = num_epochs*(len(train_dataset)/ batch_size)
n_iters = int(n_iters)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

'''
STEP 3: Building the Network
'''
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 64) #Initilization the first layer as 784.
        self.fc2 = nn.Linear(64, 32)  #Initilization of 2nd layer.
        self.fc3 = nn.Linear(32, 16)  #Initilization of 3rd layer.
        self.fc4 = nn.Linear(16, 8)    #Initilization of 4th layer.
        self.fc5 = nn.Linear(8, 10)  #Output layer of 10 neurons.
        # Dropout module with 0.2 drop probability
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        # Flattening the tensor
        x = x.view(x.shape[0], -1)

        # Now with dropout
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.dropout(F.relu(self.fc2(x)))
        x = self.dropout(F.relu(self.fc3(x)))
        x = self.dropout(F.relu(self.fc4(x)))
        # output so no dropout here
        x = F.log_softmax(self.fc5(x), dim=1)
        return x
        
model=Network()
optimizer=optim.SGD(model.parameters(),lr=0.1,weight_decay=1e-6, momentum=0.9, nesterov=True)  #setting the momentum to 0.9 so that it can land to better local minima.
criterion=nn.NLLLoss()
#optimizer=optim.Adam(model.parameters(),lr=0.01)
#optimizer=optim.SGD(model.parameters(), lr=0.02, momentum=0.9)
#optimizer=optim.SGD(model.parameters(),lr=3e-2)

## Train
epochs=num_epochs
train_losses,test_losses=[],[]
for e in range(epochs):
    running_loss=0
    for images,labels in train_loader:
        optimizer.zero_grad()
        log_ps=model(images)
        loss=criterion(log_ps,labels)
        loss.backward()
        optimizer.step()
        running_loss+=loss.item()
        
    else:
        test_loss=0
        accuracy=0
        
        with torch.no_grad():
            model.eval()
            for images,labels in test_loader:
                log_ps=model(images)
                test_loss+=criterion(log_ps,labels)
                ps=torch.exp(log_ps)
                top_p,top_class=ps.topk(1,dim=1)
                equals=top_class==labels.view(*top_class.shape)
                accuracy+=torch.mean(equals.type(torch.FloatTensor))
        model.train()
        train_losses.append(running_loss/len(train_loader))
        test_losses.append(test_loss/len(test_loader))

        print("Epoch: {}/{}.. ".format(e+1, epochs),
              "Training Loss: {:.3f}.. ".format(running_loss/len(train_loader)),
              "Test Loss: {:.3f}.. ".format(test_loss/len(test_loader)),
              "Test Accuracy: {:.3f}".format(accuracy/len(test_loader)))

print("Our model: \n\n", model, '\n')

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
plt.plot(train_losses, label='Training loss')
plt.plot(test_losses, label='test loss')
plt.legend(frameon=False)

pytorch_total_params = sum(p.numel() for p in model.parameters())
pytorch_total_params

#pytorch_total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
pytorch_trainable_params= sum(p.numel() for p in model.parameters() if p.requires_grad)
pytorch_trainable_params

