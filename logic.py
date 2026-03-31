from pathlib import Path
import random
import pandas as pd

TABLE_FILE = Path('./table.csv')
DIFFICULTIES = {
    'easy':   ['name', 'one_l', 'three_l'],
    'medium': ['name', 'one_l', 'three_l', 'iupac'],
    'hard':   ['name', 'one_l', 'three_l', 'iupac', 'smiles'],
}
SIZES = {
    'easy':   5,
    'medium': 5,
    'hard':   5,
}

def load_df():
    df = pd.read_csv(TABLE_FILE, sep=';')
    return df

def create_card_pair(df, difficulty):
    descriptors = DIFFICULTIES[difficulty]
    size = SIZES[difficulty]

    all_selection = df.sample(9).reset_index(drop=True)
    winner = all_selection.iloc[0]
    winner_descriptors = random.sample(descriptors, 2)

    decoys_a = all_selection.iloc[1:size]
    decoys_b = all_selection.iloc[size:(2*size-1)]

    cards = []
    for wd, decoys in zip(winner_descriptors, [decoys_a, decoys_b]):
        cards.append(make_card(winner['three_l'], winner[wd], decoys, descriptors))

    return winner['three_l'], cards[0], cards[1]


def make_card(winner, winner_descriptor, decoys, descriptors):
    card = []
    card.append(make_symbol(winner, winner_descriptor))
    for _, row in decoys.iterrows():
        valid_cols = [
            col for col in descriptors 
            if pd.notna(row[col]) and str(row[col]).strip().lower() != "none"
        ]
        chosen_col = random.choice(valid_cols)
        card.append(make_symbol(row['three_l'], row[chosen_col]))
    random.shuffle(card)
    return card


def make_symbol(name, desc):
    return {'name': name, 'desc': desc}


if __name__ == '__main__':
    difficulty = 'hard'
    df = load_df()
    # print(df)

    winner, card1, card2 = create_card_pair(df, difficulty)

    print(winner)
    print(card1)
    print(card2)



