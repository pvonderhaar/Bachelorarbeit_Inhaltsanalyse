# this script is to label the dialogues in the console
import sys

import inquirer
import pandas as pd


def main(filepath):
    df = pd.read_excel(filepath)
    grouped_df = df.groupby('path')

    for path_id, group in grouped_df.iterrows():
        print(f"Path ID: {path_id}")

        first_row = group.iloc[0]
        print(f"Conversation ID: {first_row['tree_id']}")

        if not df.loc['label1'].isna().any() and not df.loc['label1'].isna().any():  # funktioniert wahrscheinlich nicht
           continue  # Skip this row if it's already labeled

        for index, row in group:
            print(row['author_id'], '(', row['a/b_author'], ') :', row['text'])

main('daten/label_df.xlsx')