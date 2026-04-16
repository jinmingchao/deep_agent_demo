import torch
import torch.nn as nn
import torch.nn.functional as F


class MLP(nn.Module):
    """
    多层感知器（MLP）神经网络
    
    参数:
        input_dim: 输入特征维度
        hidden_dims: 隐藏层维度列表，例如 [64, 32, 16]
        output_dim: 输出维度
        activation: 激活函数，默认为ReLU
        dropout_rate: dropout概率，默认为0.0（无dropout）
        use_batch_norm: 是否使用批归一化，默认为False
    """
    
    def __init__(self, input_dim, hidden_dims, output_dim, 
                 activation='relu', dropout_rate=0.0, use_batch_norm=False):
        super(MLP, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.output_dim = output_dim
        self.dropout_rate = dropout_rate
        self.use_batch_norm = use_batch_norm
        
        # 选择激活函数
        if activation == 'relu':
            self.activation = nn.ReLU()
        elif activation == 'sigmoid':
            self.activation = nn.Sigmoid()
        elif activation == 'tanh':
            self.activation = nn.Tanh()
        elif activation == 'leaky_relu':
            self.activation = nn.LeakyReLU(0.01)
        else:
            raise ValueError(f"不支持的激活函数: {activation}")
        
        # 构建网络层
        layers = []
        prev_dim = input_dim
        
        # 添加隐藏层
        for i, hidden_dim in enumerate(hidden_dims):
            # 全连接层
            layers.append(nn.Linear(prev_dim, hidden_dim))
            
            # 批归一化层（如果启用）
            if use_batch_norm:
                layers.append(nn.BatchNorm1d(hidden_dim))
            
            # 激活函数
            layers.append(self.activation)
            
            # Dropout层（如果dropout_rate > 0）
            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))
            
            prev_dim = hidden_dim
        
        # 输出层（无激活函数，适用于回归任务）
        # 对于分类任务，可以在外部添加softmax或sigmoid
        layers.append(nn.Linear(prev_dim, output_dim))
        
        # 将层组合成序列
        self.network = nn.Sequential(*layers)
        
        # 初始化权重
        self._initialize_weights()
    
    def _initialize_weights(self):
        """初始化网络权重"""
        for layer in self.network:
            if isinstance(layer, nn.Linear):
                # 使用Xavier初始化
                nn.init.xavier_uniform_(layer.weight)
                if layer.bias is not None:
                    nn.init.zeros_(layer.bias)
    
    def forward(self, x):
        """
        前向传播
        
        参数:
            x: 输入张量，形状为 (batch_size, input_dim)
        
        返回:
            输出张量，形状为 (batch_size, output_dim)
        """
        return self.network(x)
    
    def get_num_parameters(self):
        """获取模型参数数量"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class MLPClassifier(MLP):
    """
    用于分类任务的MLP，在输出层添加softmax
    """
    
    def __init__(self, input_dim, hidden_dims, num_classes, 
                 activation='relu', dropout_rate=0.0, use_batch_norm=False):
        super().__init__(input_dim, hidden_dims, num_classes, 
                        activation, dropout_rate, use_batch_norm)
    
    def forward(self, x):
        """
        前向传播，返回logits（未经过softmax）
        对于分类任务，通常使用CrossEntropyLoss，它内部包含softmax
        """
        return self.network(x)
    
    def predict_proba(self, x):
        """预测概率（经过softmax）"""
        with torch.no_grad():
            logits = self.forward(x)
            return F.softmax(logits, dim=1)
    
    def predict(self, x):
        """预测类别"""
        with torch.no_grad():
            proba = self.predict_proba(x)
            return torch.argmax(proba, dim=1)


class MLPRegressor(MLP):
    """
    用于回归任务的MLP
    """
    
    def __init__(self, input_dim, hidden_dims, output_dim, 
                 activation='relu', dropout_rate=0.0, use_batch_norm=False):
        super().__init__(input_dim, hidden_dims, output_dim, 
                        activation, dropout_rate, use_batch_norm)
    
    def forward(self, x):
        """前向传播，直接返回网络输出"""
        return self.network(x)


def create_mlp_model(model_type='classifier', **kwargs):
    """
    创建MLP模型的工厂函数
    
    参数:
        model_type: 模型类型，'classifier' 或 'regressor'
        **kwargs: 传递给MLP构造函数的参数
    
    返回:
        MLP模型实例
    """
    if model_type == 'classifier':
        return MLPClassifier(**kwargs)
    elif model_type == 'regressor':
        return MLPRegressor(**kwargs)
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")