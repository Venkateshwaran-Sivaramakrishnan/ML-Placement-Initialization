import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential, layers
from tensorflow.keras.layers import Embedding, Reshape, Dense, InputLayer, MultiHeadAttention, LayerNormalization, Dropout

np.random.seed(7)
tf.random.set_seed(7)
type_dimen = 10
loc_dimen = 20
room_dimen = 20
area_dimen = 32
ada_dimen = 2
sqe_len = 10
code = 25
code_dimen = 64

def get_loc(x,y,size):
    x_min = x - size
    x_max = x + size + 1
    y_min = y - size
    y_max = y + size + 1
    return x_min,x_max,y_min,y_max

class LearningRateLogger(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self._supports_tf_logs = True

    def on_epoch_begin(self, epoch, logs=None):
        lr = float(tf.keras.backend.get_value(self.model.optimizer.learning_rate))
        print("\nEpoch %03d: Learning rate is %6.8f." % (epoch, lr))

class CustomLearningRateScheduler(tf.keras.callbacks.Callback):
        def __init__(self, schedule):
            super(CustomLearningRateScheduler, self).__init__()
            self.schedule = schedule
        def on_epoch_begin(self, epoch, logs=None):
            if not hasattr(self.model.optimizer, "lr"):
                raise ValueError('Optimizer must have a "lr" attribute.')
            lr = float(tf.keras.backend.get_value(self.model.optimizer.learning_rate))
            scheduled_lr = self.schedule(epoch, lr)
            tf.keras.backend.set_value(self.model.optimizer.lr, scheduled_lr)
            print("\nEpoch %05d: Learning rate is %6.8f." % (epoch, scheduled_lr))

class TransformerEncoder(layers.Layer):
    def __init__(self, embed_dim, hidden, num_heads, depth, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.hidden = hidden
        self.num_heads = num_heads
        self.attention = [MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim) for _ in range(depth)]
        self.dense_proj = [Sequential([Dense(hidden[0], activation="LeakyReLU"), Dense(hidden[1]),]) for _ in range(depth)]
        self.layernorm_1 = [LayerNormalization() for _ in range(depth)]
        self.layernorm_2 = [LayerNormalization() for _ in range(depth)]
        self.supports_masking = True
        self.depth = depth

    def call(self, inputs, mask=None):
        x = inputs
        for i in range(self.depth):

            attention_output = self.attention[i](query=x, value=x, key=x,)
            proj_input = self.layernorm_1[i](x + attention_output)
            proj_output = self.dense_proj[i](proj_input)
            x = self.layernorm_2[i](proj_input + proj_output)

        return x

class GeneratorEncoder(layers.Layer):
    def __init__(self, embed_dim, hidden, num_heads, depth, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.hidden = hidden
        self.num_heads = num_heads
        self.attention = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.dense_proj = Sequential([Dense(hidden[0], activation="LeakyReLU"), Dense(hidden[1]),])
        self.layernorm_1 = LayerNormalization()
        self.layernorm_2 = LayerNormalization()
        self.supports_masking = True
        self.depth = depth

    def call(self, PartialEmbed, PriorAttr, mask=None):
        x = PartialEmbed
        for _ in range(self.depth):

            attention_output = self.attention(query=x, value=PriorAttr, key=PriorAttr)
            proj_input = self.layernorm_1(x + attention_output)
            proj_output = self.dense_proj(proj_input)
            x = self.layernorm_2(proj_input + proj_output)

        out = self.dense_proj(x)
        return out

class PositionalEmbedding(layers.Layer):
    def __init__(self, sequence_length, dimension, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = Embedding(input_dim=dimension, output_dim=embed_dim)
        self.position_embeddings = Embedding(input_dim=sequence_length, output_dim=embed_dim)
        self.sequence_length = sequence_length
        self.vocab_size = dimension
        self.embed_dim = embed_dim

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs, 0)

class PositionalEmbedding_loc(layers.Layer):
    def __init__(self, sequence_length, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = Sequential([layers.InputLayer(input_shape=(sqe_len,2), dtype="int64"),layers.Embedding(input_dim=loc_dimen, output_dim=embed_dim),layers.Dense(int(embed_dim/2)),
                                    Reshape((sqe_len,embed_dim))])

        self.position_embeddings = layers.Embedding(input_dim=sequence_length, output_dim=embed_dim)
        self.sequence_length = sequence_length
        self.embed_dim = embed_dim

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs[:,:,0], 0)

class PositionalEmbedding_IMG(layers.Layer):
    def __init__(self, sequence_length, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = Sequential([InputLayer(input_shape=(sqe_len,code), dtype="int64"),Embedding(input_dim=code_dimen, output_dim=embed_dim),Dense(int(embed_dim/code)),Reshape((sqe_len,embed_dim))])
        self.position_embeddings = Embedding(input_dim=sequence_length, output_dim=embed_dim)
        self.sequence_length = sequence_length
        self.embed_dim = embed_dim

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs[:,:,0], 0)

class PositionalEmbedding_ada(layers.Layer):
    def __init__(self, sequence_length, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.token_embeddings = Dense(embed_dim)
        self.position_embeddings = Embedding(input_dim=sequence_length, output_dim=embed_dim)
        self.sequence_length = sequence_length
        self.embed_dim = embed_dim

    def call(self, inputs):
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs[:,:,0], 0)

class PositionalEmbedding_room(layers.Layer):
    def __init__(self, sequence_length, embed_dim, **kwargs):
        #super(PositionalEmbedding, self).__init__(**kwargs)
        super().__init__(**kwargs)
        self.token_embeddings = Sequential([layers.InputLayer(input_shape=(10,4), dtype="int64"),layers.Embedding(input_dim=room_dimen, output_dim=embed_dim),layers.Dense(int(embed_dim/4)),
                                    Reshape((10,embed_dim))])

        self.position_embeddings = layers.Embedding(input_dim=sequence_length, output_dim=embed_dim)
        self.sequence_length = sequence_length
        self.embed_dim = embed_dim

    def call(self, inputs):
        # length = tf.shape(inputs)[-2]
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        return embedded_tokens + embedded_positions

    def compute_mask(self, inputs, mask=None):
        return tf.math.not_equal(inputs[:,:,0], 0)

class TransformerDecoder(layers.Layer):
    
    def __init__(self, embed_dim, hidden, num_heads,depth, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.hidden = hidden
        self.num_heads = num_heads
        self.attention_1 = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.attention_2 = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.dense_proj = Sequential([Dense(hidden[0], activation="LeakyReLU"), Dense(hidden[1]),])
        self.layernorm_1 = LayerNormalization()
        self.layernorm_2 = LayerNormalization()
        self.layernorm_3 = LayerNormalization()
        self.supports_masking = True
        self.depth = depth
        self.drop = Dropout(0.5)

    def call(self, inputs, encoder_outputs, mask=None):
        causal_mask = self.get_causal_attention_mask(inputs)
        if mask is not None:
            padding_mask = tf.cast(mask[:,tf.newaxis, :], dtype="int32")
            padding_mask = tf.minimum(padding_mask, causal_mask)
        x = inputs
        for _ in range(self.depth):
            attention_output_1 = self.attention_1(query=x, value=x, key=x, attention_mask=causal_mask)
            out_1 = self.layernorm_1(x + attention_output_1)

            attention_output_2 = self.attention_2(
                query=out_1,
                value=encoder_outputs,
                key=encoder_outputs,
                attention_mask=padding_mask,)
            out_2 = self.layernorm_2(out_1 + attention_output_2)

            proj_output = self.dense_proj(out_2)
            x = self.layernorm_3(out_2 + proj_output)
        return x

    def get_causal_attention_mask(self, inputs):
        input_shape = tf.shape(inputs)
        batch_size, sequence_length = input_shape[0], input_shape[1]
        i = tf.range(sequence_length)[:, tf.newaxis]
        j = tf.range(sequence_length)
        mask = tf.cast(i >= j, dtype="int32")
        mask = tf.reshape(mask, (1, input_shape[1], input_shape[1]))
        mult = tf.concat([tf.expand_dims(batch_size, -1), tf.constant([1, 1], dtype=tf.int32)],axis=0,)
        
        return tf.tile(mask, mult)

class Transformer_Encoder_Decoder(layers.Layer):
    
    def __init__(self, embed_dim, hidden, num_heads,depth, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.hidden = hidden
        self.num_heads = num_heads
        self.attention_0 = [MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim) for _ in range(depth)]
        self.attention_1 = [MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim) for _ in range(depth)]
        self.attention_2 = [MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim) for _ in range(depth)]
        self.dense_proj = [Sequential([Dense(hidden[0], activation="LeakyReLU"), Dense(hidden[1]),]) for _ in range(depth)]
        self.layernorm_0 = [LayerNormalization() for _ in range(depth)]
        self.layernorm_1 = [LayerNormalization() for _ in range(depth)]
        self.layernorm_2 = [LayerNormalization() for _ in range(depth)]
        self.layernorm_3 = [LayerNormalization() for _ in range(depth)]
        self.supports_masking = True
        self.depth = depth
        self.drop = Dropout(0.5)

    def call(self, inputs, encoder_outputs, mask=None):

        causal_mask = self.get_causal_attention_mask(inputs)

        if mask is not None:

            padding_mask = tf.cast(mask[:,tf.newaxis, :], dtype="int32")
            padding_mask = tf.minimum(padding_mask, causal_mask)

        x = inputs

        for i in range(self.depth):

            # Partial cross-attention Predicted
            attention_output_0 = self.attention_0[i](query=encoder_outputs, value=x, key=x, attention_mask=causal_mask)
            encoder_outputs = self.layernorm_0[i](encoder_outputs + attention_output_0)

            # Predicted self-attention
            attention_output_1 = self.attention_1[i](query=x, value=x, key=x, attention_mask=causal_mask)
            out_1 = self.layernorm_1[i](x + attention_output_1)

            # Decoder cross-attention Augumented Partial
            attention_output_2 = self.attention_2[i](query=out_1,value=encoder_outputs,key=encoder_outputs,attention_mask=padding_mask)
            out_2 = self.layernorm_2[i](out_1 + attention_output_2)

            proj_output = self.dense_proj[i](out_2)
            x = self.layernorm_3[i](out_2 + proj_output)

        return x

    def get_causal_attention_mask(self, inputs):
        
        input_shape = tf.shape(inputs)
        batch_size, sequence_length = input_shape[0], input_shape[1]
        i = tf.range(sequence_length)[:, tf.newaxis]
        j = tf.range(sequence_length)
        mask = tf.cast(i >= j, dtype="int32")
        mask = tf.reshape(mask, (1, input_shape[1], input_shape[1]))
        mult = tf.concat([tf.expand_dims(batch_size, -1), tf.constant([1, 1], dtype=tf.int32)],axis=0,)
        
        return tf.tile(mask, mult)

def mlp(x, hidden_units, dropout_rate=0.1):
    for units in hidden_units:
        x = Dense(units, activation=tf.nn.gelu)(x)
        x = Dropout(dropout_rate)(x)
    return x

class VectorQuantizer(layers.Layer):
    def __init__(self, num_embeddings, embedding_dim, beta=0.25, **kwargs):
        super().__init__(**kwargs)
        self.embedding_dim = embedding_dim
        self.num_embeddings = num_embeddings
        self.beta = beta

        w_init = tf.random_uniform_initializer()
        self.embeddings = tf.Variable(initial_value=w_init(shape=(self.embedding_dim, self.num_embeddings), dtype="float32"),trainable=True,name="embeddings_vqvae")

    def call(self, x):
        input_shape = tf.shape(x)
        flattened = tf.reshape(x, [-1, self.embedding_dim])

        encoding_indices = self.get_code_indices(flattened)
        encodings = tf.one_hot(encoding_indices, self.num_embeddings)
        quantized = tf.matmul(encodings, self.embeddings, transpose_b=True)
        quantized = tf.reshape(quantized, input_shape)

        commitment_loss = tf.reduce_mean((tf.stop_gradient(quantized) - x) ** 2)
        codebook_loss = tf.reduce_mean((quantized - tf.stop_gradient(x)) ** 2)
        self.add_loss(self.beta * commitment_loss + codebook_loss)

        quantized = x + tf.stop_gradient(quantized - x)
        return quantized

    def get_code_indices(self, flattened_inputs):
        similarity = tf.matmul(flattened_inputs, self.embeddings)
        distances = (
            tf.reduce_sum(flattened_inputs ** 2, axis=1, keepdims=True)
            + tf.reduce_sum(self.embeddings ** 2, axis=0)
            - 2 * similarity)
        encoding_indices = tf.argmin(distances, axis=1)
        return encoding_indices
    