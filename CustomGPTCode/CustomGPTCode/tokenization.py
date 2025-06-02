# tokenization.py
import json

class Tokenizer:
    def __init__(self, vocab_size):
        self.vocab_size = vocab_size
        self.merges = {}
        self.vocab = {idx: bytes([idx]) for idx in range(256)}

    def load_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        tokens = text.encode('utf-8')
        self.tokens = list(map(int, tokens))

    def get_accurances_of_pairs(self, tokens):
        token_dict = {}
        for i in range(len(tokens) - 1):
            if (tokens[i], tokens[i + 1]) in token_dict:
                token_dict[(tokens[i], tokens[i + 1])] += 1
            else:
                token_dict[(tokens[i], tokens[i + 1])] = 1
        return token_dict

    def merge_pair_into_tokens(self, tokens, pair, index):
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
                new_tokens.append(index)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        return new_tokens
    def tokenize(self):
        num_merges = self.vocab_size - 256
        copy_tokens = list(self.tokens)
        #stats = {}
        for i in range(num_merges):

            stats = self.get_accurances_of_pairs(copy_tokens)
            pair = max(stats, key=stats.get)

            idx = 256 + i
            print(f"merging {pair} into a new token {idx}")
            copy_tokens = self.merge_pair_into_tokens(copy_tokens, pair, idx)
            self.merges[pair] = idx

        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]

        print("tokens length:", len(self.tokens))
        print("ids length:", len(copy_tokens))
        print(f"compression ratio: {len(self.tokens) / len(copy_tokens):.2f}X")

    def save_merges(self, file_path):
        with open(file_path, 'w') as file:
            json.dump({str(k): v for k, v in self.merges.items()}, file)

    def load_merges(self, file_path):
        with open(file_path, 'r') as file:
            self.merges = {eval(k): v for k, v in json.load(file).items()}
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]

    def decode(self, ids):
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        return text

    def encode(self, text):
        if isinstance(text, str):
            tokens = list(text.encode("utf-8"))
        elif isinstance(text, list):
            tokens = text
        else:
            3
            raise TypeError("Input should be a string or a list of tokens")

        while len(tokens) >= 2:
            stats = self.get_accurances_of_pairs(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens = self.merge_pair_into_tokens(tokens, pair, idx)
        return tokens
"""
import os

vocabsize = 300
tokenizer = Tokenizer(vocabsize)
tokenizer.load_text('dataset_1.txt')
merges_file = 'merge_test.json'
if not os.path.exists(merges_file):
    tokenizer.tokenize()
    tokenizer.save_merges(merges_file)
else:
    tokenizer.load_merges(merges_file)
"""
