#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==================== Ejemplo GeminAI ===================================
import domino
from domino import WORDS

import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense
from tensorflow.keras.models import Model

from keras_nlp.layers import TransformerEncoder

palabras = [' '.join(WORDS)]

# Tokenizar los textos y crear vocabulario
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)
tokenizer.fit_on_texts(palabras)

sequences = tokenizer.texts_to_sequences(palabras)

# Pad las secuencias para tener la misma longitud
max_len = 100
padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_len)

# Parámetros del modelo
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 16
num_heads = 2
ff_dim = 32

# Capa de entrada
inputs = Input(shape=(max_len,))

# Capa de incrustación
embedding_layer = Embedding(vocab_size, embedding_dim)
x = embedding_layer(inputs)

# Capa Transformer
transformer_layer = TransformerEncoder(intermediate_dim=64, num_layers=1, num_heads=num_heads, dff=ff_dim, rate=0.1)
x = transformer_layer(x)

# Capa de salida
x = tf.keras.layers.GlobalAveragePooling1D()(x)
outputs = Dense(1, activation='sigmoid')(x)

# Crear el modelo
model = Model(inputs=inputs, outputs=outputs)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(padded_sequences, labels, epochs=10)


# ==================== Ejemplo Chat GPT ========================

import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Embedding, Input, GlobalAveragePooling1D
from tensorflow.keras.models import Model
import numpy as np

# Definir una capa de Transformer Encoder
class TransformerEncoder(Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerEncoder, self).__init__()
        self.attention = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential(
            [Dense(ff_dim, activation="relu"), Dense(embed_dim)]
        )
        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.attention(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# Parámetros del modelo
vocab_size = 10000  # Tamaño del vocabulario
maxlen = 100  # Longitud máxima de la secuencia
embed_dim = 32  # Dimensión de los embeddings
num_heads = 2  # Número de cabezas en Multi-Head Attention
ff_dim = 32  # Dimensión de la capa feed-forward en el Transformer

# Definir la entrada
inputs = Input(shape=(maxlen,))

# Embedding + Positional Encoding
embedding_layer = Embedding(input_dim=vocab_size, output_dim=embed_dim, input_length=maxlen)
x = embedding_layer(inputs)

# Agregar la capa de Transformer Encoder
transformer_encoder = TransformerEncoder(embed_dim, num_heads, ff_dim)
x = transformer_encoder(x)

# Pooling y salida
x = GlobalAveragePooling1D()(x)
x = Dense(20, activation="relu")(x)
x = Dense(2, activation="softmax")(x)  # Para clasificación binaria

# Crear el modelo
model = Model(inputs=inputs, outputs=x)

# Compilar el modelo
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Resumen del modelo
model.summary()

# Entrenamiento (con datos ficticios para ejemplo)
# Generar algunos datos de ejemplo
X_train = np.random.randint(0, vocab_size, size=(1000, maxlen))
y_train = np.random.randint(0, 2, size=(1000,))

# Entrenar el modelo
model.fit(X_train, y_train, batch_size=32, epochs=5)
