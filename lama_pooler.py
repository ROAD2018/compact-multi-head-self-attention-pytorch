from lama import LAMA
import torch
from torch.nn import Module
from typing import Callable


class LAMAPooler(Module):
    """
    This class implements the low rank factorization multi-head self-attention mechanism detailed
    in the paper `Low Rank Factorization for Compact Multi-Head Self-Attention
    <https://arxiv.org/abs/1912.00835>`_ .
    
    Parameters
    ----------
    num_heads : ``int``, required.
        The number of attention heads to use.
    input_dim : ``int``, required.
        The size of the last dimension of the input tensor.
    activation : ``Callable``, optional (default=``torch.tanh``)
        An activation function applied after the attention calculation. Default is 
        ``torch.tanh``. Set to ``None`` to use a linear activation (i.e. no activation).
    normalize : ``bool``, optional (default: ``True``)
        If true, we normalize the computed similarities with a softmax, to return a probability
        distribution for each attention head.  If false, this is just computing a similarity score.
    bias : TODO.
    """

    def __init__(
        self,
        num_heads: int,
        input_dim: int,
        activation: Callable = torch.tanh,  
        normalize: bool = True,
        # TODO (John): How to get max_len without asking for it explicitly?
        bias: bool = False 
    ) -> None:
        super().__init__()
        self._lama = LAMA(num_heads, input_dim, activation, normalize, bias)

    def reset_parameters(self):
        self._lama.reset_parameters()

    def forward(self, input, mask=None):
        sentence_embedding_matrix = self._lama(input, mask) @ input
        return torch.flatten(sentence_embedding_matrix)