from delab_trees.delab_tree import DelabTree
from delab_trees import TreeManager
from delab_trees.exceptions import NotATreeException
from delab_trees.util import get_root
import pandas as pd
from scripts.dialogue_functions import get_dialogue_authors, dialogue_paths_to_df
from tests.test_dialogue_functions import get_basic_test_manager

mig_conversations = pd.read_csv('daten/postgres_public_delab_tweet.csv')
tw_text = mig_conversations.dropna(subset=['text'])
tw_text = tw_text[tw_text['platform']=='twitter']
tw_text = tw_text[tw_text['language']=='de']
tree_columns = ['conversation_id', 'twitter_id', 'tn_parent_id', 'in_reply_to_user_id', 'author_id', 'text',
                'created_at']
tree_df = tw_text[tree_columns].copy()
tree_column_names = ['tree_id', 'post_id', 'parent_id', 'in_reply_to_user_id', 'author_id', 'text', 'created_at']
tree_df.columns = tree_column_names
manager = TreeManager(tree_df)
dialogue_df = dialogue_paths_to_df(manager)
dialogue_df.sort_values(by=['tree_id', 'path', 'created_at'], inplace=True)
print(len(dialogue_df))
print(len(set(dialogue_df['tree_id'].tolist())))
dialogue_df.to_csv('daten/dialogue_df_de.csv')
# speicher alles als xlsx für das labeln + 3 spalten für die label

#dialogue_df['label1'] = ''
#dialogue_df['label2'] = ''
#dialogue_df.to_excel('daten/label_df.xlsx')
