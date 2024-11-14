# Adapter Info

Below contains information on the hyperparams used to train the adapters in the `model/` directory.

`adapter_10_lr0.01_negatives.pth`:

```python
adapter_kwargs = {
    'num_epochs': 10,
    'batch_size': 32,
    'learning_rate': 0.01,
    'warmup_steps': 100,
    'max_grad_norm': 1.0,
    'margin': 1.0,
    'use_negatives': True
}
```

`adapter_10_lr0.01_no_negatives.pth`:

```python
adapter_kwargs = {
    'num_epochs': 10,
    'batch_size': 32,
    'learning_rate': 0.01,
    'warmup_steps': 100,
    'max_grad_norm': 1.0,
    'margin': 1.0,
    'use_negatives': False
}
```

`adapter_5_negatives.pth`:

```python
adapter_kwargs = {
    'num_epochs': 5,
    'batch_size': 32,
    'learning_rate': 0.003,
    'warmup_steps': 100,
    'max_grad_norm': 1.0,
    'margin': 1.0,
    'use_negatives': True
}
```

`adapter_5_no_negatives.pth`:

```python
adapter_kwargs = {
    'num_epochs': 5,
    'batch_size': 32,
    'learning_rate': 0.003,
    'warmup_steps': 100,
    'max_grad_norm': 1.0,
    'margin': 1.0,
    'use_negatives': False
}
```
