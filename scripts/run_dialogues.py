from delab_trees.delab_tree import DelabTree
from delab_trees import TreeManager
from delab_trees.exceptions import NotATreeException
from delab_trees.util import get_root
import pandas as pd
from .dialogue_funtions import get_dialogue_authors


mig_conversations = pd.read_csv('../daten/mig_conversations.csv')
tw_text = mig_conversations.dropna(subset=['text'])
tw_text = tw_text[tw_text['platform']=='twitter']
tree_columns = ['conversation_id', 'twitter_id', 'tn_parent_id', 'in_reply_to_user_id', 'author_id', 'text',
                'created_at']
tree_df = tw_text[tree_columns].copy()
tree_column_names = ['tree_id', 'post_id', 'parent_id', 'in_reply_to_user_id', 'author_id', 'text', 'created_at']
tree_df.columns = tree_column_names
manager = TreeManager(tree_df)
trees = manager.trees
dialogue_dict = {}
for tree in trees.values():
    dialogues = get_dialogue_authors(tree)
    dialogue_dict[tree.conversation_id] = dialogues
print(dialogue_dict)