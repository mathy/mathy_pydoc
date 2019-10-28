import tensorflow as tf

from .multi_head_attention import MultiHeadAttention
from .densenet_stack import DenseNetStack


class MultiHeadAttentionStack(tf.keras.layers.Layer):
    """Stack of Multi-Head Attention layers with a shared DenseNet stack
    between each layer"""

    def __init__(
        self,
        num_layers=2,
        num_heads=4,
        dropout_rate=0.1,
        attn_width=128,
        return_attention=False,
        **kwargs,
    ):
        super(MultiHeadAttentionStack, self).__init__(**kwargs)
        self.stack_height = num_layers
        self.return_attention = return_attention
        self.norm = tf.keras.layers.LayerNormalization(name=f"{self.name}_layer_norm")
        self.add = tf.keras.layers.Add()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
        self.memory = DenseNetStack(
            name=f"{self.name}_densenet",
            output_transform=tf.keras.layers.Dense(units=attn_width),
        )
        self.stack = []
        for i in range(self.stack_height):
            self.stack.append(
                MultiHeadAttention(
                    num_heads,
                    trainable=True,
                    name=f"{self.name}_{i}",
                    return_attention=return_attention,
                )
            )

    def compute_output_shape(self, input_shape):
        return tf.TensorShape([input_shape[0], None])

    def call(self, input_tensor: tf.Tensor):
        stack = self.stack
        attentions = []
        output = input_tensor
        for layer in stack:
            if self.return_attention:
                attn_out, attn_weights = layer(output)
                attentions.append(attn_weights)
                output = in_one = attn_out
            else:
                output = in_one = layer(output)
            output = self.dropout(output)
            output = in_two = self.norm(self.add([in_one, output]))
            output = self.memory(output)
            output = self.norm(self.add([in_two, output]))
        if self.return_attention:
            return output, attentions
        return output
