import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import inflection

def load_dataset(path):
    df = pd.read_csv(path)
    df.columns = [inflection.underscore(var) for var in list(df.columns)]
    return df

def acc_risk_idx(df):
    df = df.copy()
    groupby_postcode = df[['postcode', 'number_of_casualties']].groupby('postcode').agg(['count', 'sum', 'mean'])
    groupby_postcode = groupby_postcode.reset_index()
    groupby_postcode.columns = ['postcode', 'accident_count', 'total_casualties', 'accident_risk_index']
    return groupby_postcode.sort_values(by='total_casualties', ascending=False).reset_index(drop=True)

def merge_dataset(df1, df2):
    df1 = df1.copy()
    return df1.merge(
        df2[['postcode', 'accident_risk_index']],
        how='inner',
        on = 'postcode'
    )

def missing_values(df):
    table = pd.DataFrame(
        columns=['variable',
                 'unique_values',
                 'pandas_dtype',
                 'missing_value',
                 '%_missing_values']
    )

    for i, var in enumerate(df.columns):
        table.loc[i] = [var,
                        df[var].nunique(),
                        df[var].dtypes,
                        df[var].isnull().sum(),
                        df[var].isnull().sum() * 100 / df.shape[0],
        ]
    return table

def num_descriptive_analysis(df):
    # use pandas describe
    desc = df.describe().round(2).T.reset_index()
    desc.columns = ['variable', 'count', 'mean', 'std',
                    'min', '25%', '50%', '75%', 'max']
    # drop the count
    desc = desc.drop('count', axis=1)

    # add max, range, IQR, mode, kurtosis, and skewness
    def interquartile_range(series):
        q3, q1 = np.percentile(series, [75 ,25])
        return np.round(q3 - q1, 2)

    new_desc = pd.DataFrame(
        columns=['variable', 'range', 'IQR',
                 'mode', 'kurtosis', 'skewness']
    )
    for i, var in enumerate(df.select_dtypes(np.number).columns):
        new_desc.loc[i] = [var,
                          df[var].max() - df[var].min(),
                          interquartile_range(df[var]),
                          df[var].mode()[0],
                          df[var].kurtosis().round(2),
                          df[var].skew().round(2)
        ]

    # display both table
    desc = desc.set_index('variable')
    new_desc = new_desc.set_index('variable')
    display(desc.T)
    print()
    display(new_desc.T)

def single_violinplot(df, var, max_count=None, count_step=None):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    colors = ['#99d594', '#D53E4F', '#FC8D59']
    sns.violinplot(data=df, x=var, ax=ax, color=colors[0])
    for location in ['top', 'left', 'right']:
        ax.spines[location].set_visible(False)

    ax.set_axisbelow(True)
    ax.set_xlabel("")
    ax.set_xlabel(inflection.titleize(var), fontsize=14)
    #ax.set_ylabel("Count", fontsize=14)
    #ax.set_xlim(0, 6, 0.5)

    plt.xticks(alpha=1, fontsize=14)
    plt.yticks(alpha=1, fontsize=14)
    plt.grid(axis='x', alpha=0.3)

def single_countplot(df, var):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    colors = ['#99d594', '#D53E4F', '#FC8D59']
    sns.countplot(data=df, x=var, ax=ax, color=colors[0])
    feat_counts = df[var].value_counts().sort_index().values
    for n, count in enumerate(feat_counts):
        ax.annotate(
              f"{(100* count/np.sum(feat_counts)):.1f}%",
              xy=(n, count + 7000),
              color='#4a4a4a', fontsize=14, alpha=1,
              va = 'center', ha='center',
        )
        for location in ['top', 'right']:
            ax.spines[location].set_visible(False)
        ax.grid(axis='y', alpha=0.2)
        ax.set_axisbelow(True)
        ax.set_xlabel(f"{inflection.titleize(var)}", fontsize=14)
        ax.set_ylabel("Count", fontsize=14)
        ax.set_ylim(0, 350001, 50000)

    plt.xticks(alpha=1, fontsize=14)
    plt.yticks(alpha=1, fontsize=14)
    plt.grid(axis='y', alpha=0.5)

def single_vcountplot(df, var, n_row=0):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    colors = ['#99d594', '#D53E4F', '#FC8D59']
    sns.countplot(data=df, y=var, ax=ax, color=colors[0])
    total = df[var].count()
    for p in ax.patches:
        ax.annotate(
            f"{p.get_width() / total * 100 :.1f}%",
            xy=(p.get_width(), p.get_y()+p.get_height()/2),
            xytext=(5, 0), textcoords='offset points',
            ha="left", va="center", fontsize=14
        )
    for location in ['top', 'right']:
        ax.spines[location].set_visible(False)
    ax.grid(axis='x', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_ylabel("")
    ax.set_xlabel("Count", fontsize=14)
    ax.set_xlim(0, 500001, 50000)
    plt.xticks(alpha=1, fontsize=14)
    plt.yticks(alpha=1, fontsize=14)
