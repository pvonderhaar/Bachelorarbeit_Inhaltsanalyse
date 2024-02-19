from delab_trees.delab_tree import DelabTree
from delab_trees import TreeManager
from delab_trees.exceptions import NotATreeException
from delab_trees.util import get_root
import pandas as pd
from scripts.dialogue_functions import dialogue_paths_to_df, label_author_flow
from tests.test_dialogue_functions import get_basic_test_manager

data_df = pd.read_excel('daten/label_df_2Runde.xlsx')
print(len(data_df))
grouped_df = data_df.groupby(['tree_id', 'path']                             )
new_df = pd.DataFrame()
for name1, path in grouped_df:
    new_path_df = label_author_flow(path)
    new_df = pd.concat([new_df, new_path_df])

new_df.to_excel('daten/Runde_2_clean.xlsx')





