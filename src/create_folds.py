import pandas as pd
from sklearn.model_selection import StratifiedKFold

def kfold_setup(df, target):
    seed = 1

    df['k_folds'] = -1
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    y = df[target].values

    k = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)

    for fold, (train_index, val_index) in enumerate(k.split(X=df, y=y)):
        df.loc[val_index, 'k_folds'] = fold

    return df.to_csv(f'./input/train_folds.csv', index=False)

if __name__ == '__main__':
    df = pd.read_csv("./input/train_mod.csv")
    kfold_setup(df, target='accident_risk_index')



























# end
