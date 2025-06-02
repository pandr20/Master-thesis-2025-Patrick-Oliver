import pandas as pd
from scipy.stats import pearsonr, linregress
import matplotlib.pyplot as plt

# Your nested dictionary
data = {
    'prompt_engineering_q_1': {'votes': 13, 'length': 423},
    'naive_rag_q_1': {'votes': 0, 'length': 60},
    'advanced_rag_q_1': {'votes': 1, 'length': 2068},
    'fine_tuning_q_1': {'votes': 7, 'length': 253},
    'prompt_engineering_q_2': {'votes': 9, 'length': 1069},
    'naive_rag_q_2': {'votes': 3, 'length': 975},
    'advanced_rag_q_2': {'votes': 1, 'length': 1804},
    'fine_tuning_q_2': {'votes': 7, 'length': 412},
    'prompt_engineering_q_3': {'votes': 9, 'length': 403},
    'naive_rag_q_3': {'votes': 4, 'length': 696},
    'advanced_rag_q_3': {'votes': 3, 'length': 1268},
    'fine_tuning_q_3': {'votes': 6, 'length': 207},
    'prompt_engineering_q_4': {'votes': 9, 'length': 319},
    'naive_rag_q_4': {'votes': 13, 'length': 435},
    'advanced_rag_q_4': {'votes': 0, 'length': 1329},
    'fine_tuning_q_4': {'votes': 3, 'length': 232},
    'prompt_engineering_q_5': {'votes': 9, 'length': 320},
    'naive_rag_q_5': {'votes': 10, 'length': 574},
    'advanced_rag_q_5': {'votes': 2, 'length': 1181},
    'fine_tuning_q_5': {'votes': 4, 'length': 178},
    'prompt_engineering_q_6': {'votes': 10, 'length': 592},
    'naive_rag_q_6': {'votes': 6, 'length': 406},
    'advanced_rag_q_6': {'votes': 4, 'length': 1121},
    'fine_tuning_q_6': {'votes': 3, 'length': 189},
    'prompt_engineering_q_7': {'votes': 7, 'length': 1155},
    'naive_rag_q_7': {'votes': 9, 'length': 711},
    'advanced_rag_q_7': {'votes': 0, 'length': 2172},
    'fine_tuning_q_7': {'votes': 7, 'length': 256},
    'prompt_engineering_q_8': {'votes': 11, 'length': 443},
    'naive_rag_q_8': {'votes': 6, 'length': 293},
    'advanced_rag_q_8': {'votes': 3, 'length': 1715},
    'fine_tuning_q_8': {'votes': 2, 'length': 202},
    'prompt_engineering_q_9': {'votes': 9, 'length': 356},
    'naive_rag_q_9': {'votes': 11, 'length': 340},
    'advanced_rag_q_9': {'votes': 1, 'length': 987},
    'fine_tuning_q_9': {'votes': 2, 'length': 177},
    'prompt_engineering_q_10': {'votes': 14, 'length': 871},
    'naive_rag_q_10': {'votes': 3, 'length': 2000},
    'advanced_rag_q_10': {'votes': 2, 'length': 1257},
    'fine_tuning_q_10': {'votes': 3, 'length': 248}
}

# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Get x and y
x = df['length']
y = df['votes']

# Pearson correlation
correlation, p_value = pearsonr(x, y)


# Plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y, label='Data points')
plt.xlabel('Response Length (chars)')
plt.ylabel('Votes')
plt.title('Votes vs. Response Length')
plt.grid(True)
plt.legend()

# Annotate correlation
plt.text(
    0.05, 0.95,
    f"Pearson r = {correlation:.2f}",
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment='top',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.7)
)

plt.show()