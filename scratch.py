def create_folds(df, seed=0):
    df = df.copy()
    df["k_fold"] = -1

    k = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    X = df.drop('default_payment_next_month', axis=1)
    y = df['default_payment_next_month']

    for fold, (train_idx, val_idx) in enumerate(k.split(X, y)):
        df.loc[val_idx, 'k_fold'] = fold

    return df

def train_the_model(
    fold,
    df=None,
    target=None,
    drop_features=None,
    preprocessor=None,
    model=None,
):
    if df is None:
       df = pd.read_csv("../input/full_train_folds.csv")

    if df.isnull().sum().sum() > 0:
       df = df.fillna("-1")

    features = [
        var for var in df.columns if var not in drop_features
    ]

    train = df[df['k_fold'] != fold].reset_index(drop=True)
    val = df[df['k_fold'] == fold].reset_index(drop=True)

    full_train = pd.concat(
        [train, val], axis=0
    )
    preprocessor.fit(full_train[features])

    X_train = preprocessor.transform(train[features])
    X_val = preprocessor.transform(val[features])

    y_train = train[target].values
    y_val = val[target].values

    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_val)[:, 1]

    auc = roc_auc_score(y_val, y_pred)
    print(f"Fold-{fold} | AUC = {auc:.3f}")

    with open('../models/model_dtc.bin', 'wb') as f_out:
         pickle.dump({
            'preprocessor': preprocessor,
            'model': model,
            'val_auc': auc
         })

def main():
    df = create_folds(full_train)
    drop_features = [
        'id', 'default_payment_next_month', 'k_fold'
    ]
    preprocessor = StandardScaler()
    clf = DecisionTreeClassifier(max_depth=7, random_state=seed)
    train_the_model(
        fold=3,
        df=df,
        target='default_payment_next_month',
        drop_features=drop_features,
        preprocessor=preprocessor,
        model=clf
    )

main()































# end of code
