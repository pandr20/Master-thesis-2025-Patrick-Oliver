import torch
import torch.nn as nn
import time
import os

#from pycparser.ply.yacc import token
from torch.nn import functional as F, Dropout
import json

from tokenization import Tokenizer
#from fastapi import FastAPI

vocab_size = 8000

batch_size = 128

block_size = 64
max_iters = 10000
eval_interval = 500
learning_rate = 1e-4
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters =200


n_embd = 768

n_head = 8
n_layer = 8




dropout = 0.1

merges_file = 'merge_dataset_10_2000.json'


dataset_file = 'dataset_10.txt'

#--------------
hyperparameters = {
    'batch_size': batch_size,
    'block_size': block_size,
    'max_iters': max_iters,
    'eval_interval': eval_interval,
    'learning_rate': learning_rate,
    'device': device,
    'eval_iters': eval_iters,
    'n_embd': n_embd,
    'n_head': n_head,
    'n_layer': n_layer,
    'dropout': dropout,
    'vocab_size': vocab_size,
    'merges_file': merges_file,
    'dataset_file': dataset_file
}
#torch.manual_seed(1337)

print(device)
start_time = time.time()

#Manual compression of tokens
"""
tokenizer = Tokenizer(vocab_size)
tokenizer.load_text(dataset_file)


if not os.path.exists(merges_file):
    print('tokenizing')
    tokenizer.tokenize()
    print('saving merges')
    tokenizer.save_merges(merges_file)


else:
    print('loading merges')
    tokenizer.load_merges(merges_file)

"""
#Word tokenization
with open(dataset_file, 'r', encoding="utf-8") as file:
    text = file.read()
words = text.split()
words = sorted(list(set(words)))
vocab_size = len(words)

print(f"Number of unique words: {vocab_size}")

stoi = { word: i for i, word in enumerate(words) }
itos = { i: word for i, word in enumerate(words) }
encode = lambda s: [stoi[word] for word in s.split()]
decode = lambda l: ' '.join(itos[i] for i in l)
"""
#Character tokenization

chars = sorted(list(set(text)))
vocab_size = len(chars)
#create a mapping from characters to integers
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[ch] for ch in s]
decode = lambda l: ''.join(itos[i] for i in l)
"""
"""
if os.path.exists('encoded_' + dataset_file + '_'+ merges_file + '.pt'):
    print('loading encoded data')
    data = torch.load('encoded_' + dataset_file + '_'+ merges_file + '.pt')
    #print(data[:100])
else:
    print('encoding data')
    data = torch.tensor(tokenizer.encode(tokenizer.tokens), dtype=torch.long)
    print('saving encoded data')
    torch.save(data, 'encoded_' + dataset_file + '_'+ merges_file + '.pt')
"""
data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9*len(data))
train_data = data[:n]
val_data = data[n:]

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        accuracies = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()

            # Calculate accuracy
            if len(logits.shape) == 2:
                # Already flattened logits
                preds = torch.argmax(logits, dim=-1)
                targets = Y.reshape(-1)  # Flatten targets
            else:
                # Need to reshape logits
                B, T, C = logits.shape
                logits = logits.reshape(B * T, C)
                preds = torch.argmax(logits, dim=-1)
                targets = Y.reshape(B * T)

            correct = (preds == targets).float().mean()
            accuracies[k] = correct.item()

        out[split + '_loss'] = losses.mean()
        out[split + '_acc'] = accuracies.mean()
    model.train()
    return out

class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)
    def forward(self,x):
        B,T,C = x.shape
        k = self.key(x)
        q = self.query(x)
        wei = q @ k.transpose(-2,-1) * C**-0.5
        wei = wei.masked_fill(self.tril[:T,:T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1)
        wei = self.dropout(wei)
        v = self.value(x)
        out = wei @ v
        return out
class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)
    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out
class FeedForward(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout)

        )
    def forward(self, x):
        return self.net(x)
class Block(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        head_size = n_embd// n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedForward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)
    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x
class BigramLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)
    def forward(self, idx, targets=None):
        B, T = idx.shape

        tok_emd = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device))
        x = tok_emd + pos_emb
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T,C)
            targets = targets.view(B*T)

            loss = F.cross_entropy(logits, targets)

        return logits, loss
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:,-block_size:]
            logits, loss = self(idx_cond)
            logits = logits[:,-1,:]
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx,idx_next), dim = 1)
        return idx
model = BigramLanguageModel()

m = model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)


print(f"Total number of parameters: {sum(p.numel() for p in model.parameters())}")
context = torch.zeros((1, 1), dtype=torch.long, device=device)


def save_model_with_version(model, directory='./', base_name='model_state_dict', hyperparameters=None, training_time=None, final_losses=None):
    version = get_next_version(base_name, directory)
    while os.path.exists(os.path.join(directory, f"{base_name}_v{version}.pth")):
        version += 1
    file_path = os.path.join(directory, f"{base_name}_v{version}.pth")
    torch.save(model.state_dict(), file_path)
    print(f"Model saved as {file_path}")

    if hyperparameters is not None and training_time is not None and final_losses is not None:
        final_losses = {k: float(v) for k, v in final_losses.items()}
        metadata = {
            'hyperparameters': hyperparameters,
            'training_time': training_time,
            'final_losses': final_losses
        }
        print(final_losses)
        metadata_file_path = os.path.join(directory, f"{base_name}_v{version}_metadata.json")
        with open(metadata_file_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata saved as {metadata_file_path}")


from fastapi import FastAPI

app = FastAPI()

def load_model():
    model.load_state_dict(torch.load('./model_state_dict_v41.pth', weights_only=True))
    hardcoded_inputs = [#"Hvilke AI-tools anbefaler I til contentproduktion og kundeservice og kan jeg lære dem via jer?",
                       #"Hvordan fungerer jeres AI-coaching og hvad lærer jeg konkret?",
                       "Hvordan adskiller jeres AI-løsninger sig fra andre bureauers?",
                       #"Er det muligt at få skræddersyet AI-setup eller undervisning kun til min branche eller arbejdsproces?",
                       #"Hvilket annonceringsbudget skal jeg minimum regne med for at få resultater?",
                       #"Hvordan foregår et typisk samarbejde med jer fra start til slut?",
                       #"Kan I hjælpe med alt hvis jeg ikke har nogen marketingopsætning i forvejen?",
                       "Hvad sker der hvis jeg ikke er tilfreds med jeres arbejde?",
                       "Hvilke resultater har I tidligere skabt og hvad kan jeg realistisk forvente?",
                        "Kan I hjælpe mig med at automatisere mine arbejdsgange med AI og i så fald hvordan?"]
    output_list = []
    for x in hardcoded_inputs:
        context = torch.tensor([encode(x)], dtype=torch.long, device=device)
        generated_tokens = m.generate(context, max_new_tokens=50)[0].tolist()
        print(decode(generated_tokens))
    return output_list

@app.post("/chatbot")
async def read_root():
    response = load_model()
    return {"message": response}

def get_next_version(base_name='model_state_dict', directory='./'):
    version = 1
    while os.path.exists(os.path.join(directory, f"{base_name}_v{version}.pth")):
        version += 1
    return version

import matplotlib.pyplot as plt


def train_model():
    iter_start_time = time.time()
    train_losses = []
    val_losses = []
    train_accuracies = []
    val_accuracies = []


    for iter in range(max_iters):
        print(f"iteration {iter}")
        if iter % eval_interval == 0:
            metrics = estimate_loss()
            train_losses.append(metrics['train_loss'])
            val_losses.append(metrics['val_loss'])
            train_accuracies.append(metrics['train_acc'])
            val_accuracies.append(metrics['val_acc'])
            print("Evaluation metrics:")
            print(f"train loss: {metrics['train_loss']:.4f}, train acc: {metrics['train_acc']:.4f}")
            print(f"val loss: {metrics['val_loss']:.4f}, val acc: {metrics['val_acc']:.4f}")
            print(f"step {iter}: train loss {metrics['train_loss']:.4f}, val loss {metrics['val_loss']:.4f}")
            iter_end_time = time.time()
            iter_elapsed_time = iter_end_time - iter_start_time
            iter_start_time = time.time()
            print(f"Iteration {iter} time: {iter_elapsed_time:.2f} seconds")

        xb, yb = get_batch('train')
        logits, loss = m(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Training time: {elapsed_time:.2f} seconds")
    final_losses = estimate_loss()

    save_model_with_version(m, hyperparameters=hyperparameters, training_time=elapsed_time, final_losses=final_losses)
    version = get_next_version()

    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(range(0, max_iters, eval_interval), train_losses, label='Train Loss')
    plt.plot(range(0, max_iters, eval_interval), val_losses, label='Validation Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(range(0, max_iters, eval_interval), train_accuracies, label='Train Accuracy')
    plt.plot(range(0, max_iters, eval_interval), val_accuracies, label='Validation Accuracy')
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    graph_filename = f"metrics_graph_v{version}.png"
    plt.savefig(graph_filename)
    plt.show()
#response = load_model()
train_model()

