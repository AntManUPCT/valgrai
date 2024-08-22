#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.optim as optim

from domino import WORDS

# Parámetros del modelo
embedding_dim = 128  # Dimensión del embedding
num_heads = 4        # Número de cabezas en la capa de atención multi-cabeza
num_layers = 1       # Número de capas en el Transformer
dropout = 0.1        # Probabilidad de dropout

# Definir la arquitectura del modelo
class TransformerModel(nn.Module):
    def __init__(self, input_dim, embedding_dim, num_heads, num_layers, dropout):
        super(TransformerModel, self).__init__()

        # Embedding de la entrada
        self.embedding = nn.Embedding(input_dim, embedding_dim)

        # Capa de Positional Encoding (opcional, pero mejora rendimiento)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 500, embedding_dim))

        # Definir una capa de TransformerEncoder
        encoder_layers = nn.TransformerEncoderLayer(embedding_dim, num_heads, dim_feedforward=512, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)

        # Capa final de clasificación
        self.fc = nn.Linear(embedding_dim, 2)  # Asumiendo 2 valores de salida (Probabilidades de ganar/perder)

    def forward(self, x):
        x = self.embedding(x) + self.pos_encoder[:, :x.size(1), :]
        x = self.transformer_encoder(x)
        x = x.mean(dim=1)  # Promedio sobre la dimensión de secuencia
        x = self.fc(x)
        return x

# Parámetros del modelo
input_dim = len(WORDS)  # Tamaño del vocabulario
model = TransformerModel(input_dim, embedding_dim, num_heads, num_layers, dropout)

# Ejemplo de entrada
input_seq = torch.randint(0, input_dim, (32, 50))  # Batch de 32 secuencias de longitud 50
print(input_seq.shape)  # Esto debería imprimir: torch.Size([32, 50])

# Hacer una pasada hacia adelante con el modelo
output = model(input_seq)

print(output.shape)  # Esto debería imprimir: torch.Size([32, 2])
print('output: ', output)

# Entrenamiento

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Ejemplo de entrenamiento con un solo paso
output = model(input_seq)
loss = criterion(output, torch.randint(0, 2, (32,)))  # Etiquetas aleatorias
loss.backward()
optimizer.step()
