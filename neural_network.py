"""
Created on September 17th

@author: David Gayowsky

Simple neural network using PyTorch to process signal data: classification algorithm.
"""

#######################################################################

import numpy as np
import math 
import torch
import matplotlib.pyplot as plt
import copy
import os
import torch.optim as optim
import torch.nn as nn
from torch.nn import Linear, ReLU, Sigmoid, Module, BCELoss, Softmax
from torch import Tensor
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import itertools
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
#DONT!! USE CUDA UNLESS YOU'RE ME (DAVID)
device = 'cpu'

#######################################################################

'''Args:
p: number of sensor inputs
input_data_array: any given array of data
all_sensor_data: position data from glove sensors of size P, where for all p in p, len(p) >=  1
all_recorded_outputs: outputs corresponding to each point of position data of size P
all_possible_outputs: all possible outputs, e.g. for all p in P, p in all_possible_outputs
y: number of possible outputs
loss_fn: loss function
optimizer: optimizer
network passes: number of epochs over network we perform
learning rate: learning rate'''

p = 7
y = 5

#######################################################################

#Define function to add elements on to the end of a list.
def merger(seglist):
  total_list = []
  for seg in seglist:
    #Add given elements of input list to the end.
    total_list.extend(seg)
  return total_list

#Define a function to receive data from file.
def extract_data():
     return 

#Define a function to convert our data into a tensor.
#Note that we can use this to convert any array into a tensor.

def convert_data(input_data_array):

    #Basically we just throw this in a pytorch tensor.
    data_tensor = torch.tensor(input_data_array)
                                
    return data_tensor

#Define a function to split data into training and testing data.
#We don't necessarily need this, but it's nice to have! 
#def training_testing_data(all_sensor_data, all_recorded_outputs, all_possible_outputs):
     
    #Create index IDs and shuffle them, then grab half of them to be training data.
    #index_ids = np.arange(len(all_recorded_outputs))
    #np.random.shuffle(index_ids)
    #train_indices = index_ids[:math.floor(0.5*len(all_sensor_data))]
    #training_data = all_sensor_data[train_indices]

    #... ad nauseum, I won't finish this function for now because we don't really need 
    #this for the purposes of this hackathon.

#######################################################################

#Initializing neural network code:

#Create class for our NN:
class NeuralNetwork(nn.Module):
    
    #Define neural network structure with init:
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.layer_1 = nn.Linear(p, 16+p) 
        self.activation_1 = nn.ReLU()
        self.layer_2 = nn.Linear(16+p, 32+p) 
        self.activation_2 = nn.ReLU()
        self.layer_out = nn.Linear(32+p, y)
        self.activation_out = nn.Tanh()

    #Define forward pass across layers with functions:
    def forward(self, inputs):
        x = self.activation_1(self.layer_1(inputs))
        x = self.activation_2(self.layer_2(x))
        x = self.activation_out(self.layer_out(x))
        return x
    
#Define a function to train our neural network.
def train_NN(model, loss_fn, optimizer, training_pass_loss, training_sensor_data, training_output_data):
    
    #Put it into training mode:
    model.train()
    
    #Send our training data to device:
    training_sensor_data = training_sensor_data.to(device)
    training_output_data = training_output_data.type(torch.LongTensor)
    training_output_data = training_output_data.to(device)
    optimizer.zero_grad()

    #Compute predicted outputs given the sensor data:
    predicted_outputs = model(training_sensor_data.float())
    
    #Compute loss between our energy values and our predicted energies:
    train_loss = loss_fn(predicted_outputs, training_output_data)
    #Complete backwards pass:
    train_loss.backward()
    optimizer.step()
    training_pass_loss += train_loss.item()

    return training_pass_loss

#Define a function to pass data to our neural network during training.
def pass_to_NN_training(network_passes, learning_rate, all_sensor_data, all_recorded_outputs, all_possible_outputs):
    
    #Grab device or whatever, I don't know, we just have to do it.
    model = NeuralNetwork().to(device)
    
    #Declare loss function and optimizer we'd like to use.
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), learning_rate)

    #Convert our data to tensors:
    training_sensor_data = convert_data(all_sensor_data)
    training_output_data = convert_data(all_recorded_outputs)
    training_output_data = convert_data(all_possible_outputs)
    
    #Initialize loss value.
    training_pass_loss = 0
    #Initialize array to store our loss values.
    training_losses = []
    
    #Make our training passes over the network.
    for i in range(1, network_passes+1):
        #Call our training NN.
        training_step_loss = train_NN(model, loss_fn, optimizer, training_pass_loss, training_sensor_data, training_output_data)
        #And append it to an array to store it.
        training_losses.append(training_step_loss)

    #INSERT FUNCTION HERE TO RETURN WEIGHTS
    
    return training_losses

#Write a function to save our trained neural network weights.
def save_weights(weights):

    return

#######################################################################

#Actual neural network code, aka we're passing stuff to the neural network:

#Write a function to load our trained neural network weights.
def load_weights():

    return

#Define a function to actually classify some data.
def classify_data(model, test_sensor_data):

    #Convert our test sensor data to a pytorch tensor:
    test_sensor_data = convert_data(test_sensor_data)

    #Load and assign our weights:
    model_weights = load_weights()
    model.layer_1.weight = torch.nn.Parameter(model_weights)

    #Initialize output list:
    output_pred_list = []
        
    with torch.no_grad():
        #Put our model into testing mode:
        model.eval()
        test_sensor_data = test_sensor_data.to(device)
        #Generate our predicted outputs:
        outputs_test_pred = model(test_sensor_data.float())
        #??? (x-files theme music plays)
        _, output_pred_tags = torch.max(outputs_test_pred, dim = 1)
        output_pred_list.append(output_pred_tags.cpu().numpy())
    
    if len(output_pred_list) > 1:
        output_pred_list = [a.squeeze().tolist() for a in output_pred_list]
        #Well we throw all these lists together here.
        output_pred_list = merger(output_pred_list)
    
    return output_pred_list

#######################################################################

#Stuff we actually have to run idk gworl I'm so tired:

#1. Extract training data from a file.

#2. Train neural network using pass_to_NN_training

#3. Save weights.

#4. Extract testing data from a file.

#6. Pass testing data to classify_data (which has in-built load weights function - note have to specify file path).