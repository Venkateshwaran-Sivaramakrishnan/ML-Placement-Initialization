import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Dense, Concatenate, Embedding, Add, Flatten
from tensorflow.keras.layers import Activation, LeakyReLU, Reshape
from tensorflow.keras.models import Model,load_model

class VectorQuantizer(layers.Layer):
    def __init__(self, num_embeddings, embedding_dim, beta=0.25, **kwargs):
        super().__init__(**kwargs)
        self.embedding_dim = embedding_dim
        self.num_embeddings = num_embeddings

        # The `beta` parameter is best kept between [0.25, 2] as per the paper.
        self.beta = beta

        # Initialize the embeddings which we will quantize.
        w_init = tf.random_uniform_initializer()
        self.embeddings = tf.Variable(
            initial_value=w_init(
                shape=(self.embedding_dim, self.num_embeddings), dtype="float32"
            ),
            trainable=True,
            name="embeddings_vqvae",
        )

    def call(self, x):
        # Calculate the input shape of the inputs and
        # then flatten the inputs keeping `embedding_dim` intact.
        input_shape = tf.shape(x)
        flattened = tf.reshape(x, [-1, self.embedding_dim])

        # Quantization.
        encoding_indices = self.get_code_indices(flattened)
        encodings = tf.one_hot(encoding_indices, self.num_embeddings)
        quantized = tf.matmul(encodings, self.embeddings, transpose_b=True)

        # Reshape the quantized values back to the original input shape
        quantized = tf.reshape(quantized, input_shape)

        commitment_loss = tf.reduce_mean((tf.stop_gradient(quantized) - x) ** 2)
        codebook_loss = tf.reduce_mean((quantized - tf.stop_gradient(x)) ** 2)
        self.add_loss(self.beta * commitment_loss + codebook_loss)

        # Straight-through estimator.
        quantized = x + tf.stop_gradient(quantized - x)
        return quantized

    def get_code_indices(self, flattened_inputs):
        # Calculate L2-normalized distance between the inputs and the codes.
        similarity = tf.matmul(flattened_inputs, self.embeddings)
        distances = (
            tf.reduce_sum(flattened_inputs ** 2, axis=1, keepdims=True)
            + tf.reduce_sum(self.embeddings ** 2, axis=0)
            - 2 * similarity
        )

        # Derive the indices for minimum distances.
        encoding_indices = tf.argmin(distances, axis=1)
        return encoding_indices

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract VQ-VAE codebook indices from image(s).")
    parser.add_argument('--count', type=int, default=1, help='Number of images to process (default: 1)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    encoder = load_model('VQ_Pretrained/mix_5564/vqvae_en/encoder.keras')
    decoder = load_model('VQ_Pretrained/mix_5564/vqvae_de/decoder.keras')
    vq_value = np.load('VQ_Pretrained/mix_5564/vqvae_q/quantizer.npy')
    quantizer = VectorQuantizer(64, 64)
    quantizer.embeddings = tf.Variable(
                initial_value=vq_value,
                trainable=False,
                name="embeddings_vqvae",
            )

    np_codebooks = np.zeros((args.count,25))

    for i in range(args.count):
        img_path = f'{i}.jpg'
        img = image.load_img(img_path, color_mode='rgba', target_size=(128, 128))
        x1 = image.img_to_array(img)
        x = x1/255.
        x2 = np.expand_dims(x, axis=0)
        encoded_outputs = encoder.predict(x2)
        flat_enc_outputs = encoded_outputs.reshape(-1, encoded_outputs.shape[-1])
        codebook_indices = quantizer.get_code_indices(flat_enc_outputs).numpy()
        np_codebooks[i] = codebook_indices
    np.save('RPLAN_B.npy',np_codebooks.astype(np.int32))

if __name__ == '__main__':
    main()