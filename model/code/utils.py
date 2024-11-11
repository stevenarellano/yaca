import json

from torch.utils.data import Dataset
from torch import nn


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_config(path="../config.json"):
    with open(path, "r") as f:
        return json.load(f)


class LinearAdapter(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, input_dim)

    def forward(self, x):
        return self.linear(x)


class TripletDataset(Dataset):
    def __init__(self, data, base_model):
        self.data = data
        self.base_model = base_model

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        query = item['problem']
        positive = item['solution']
        negative = item['non_optimal_solution']

        query_emb = self.base_model.encode(query, convert_to_tensor=True)
        positive_emb = self.base_model.encode(positive, convert_to_tensor=True)
        negative_emb = self.base_model.encode(negative, convert_to_tensor=True)
        return query_emb, positive_emb, negative_emb


class DupletDataset(Dataset):
    def __init__(self, data, base_model):
        self.data = data
        self.base_model = base_model

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        query = item['problem']
        positive = item['solution']

        query_emb = self.base_model.encode(query, convert_to_tensor=True)
        positive_emb = self.base_model.encode(positive, convert_to_tensor=True)
        return query_emb, positive_emb
