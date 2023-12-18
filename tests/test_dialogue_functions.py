import unittest
from scripts.dialogue_functions import dialogue_paths_to_df
from delab_trees.delab_tree import DelabTree
from delab_trees import TreeManager
import pandas as pd
from datetime import datetime


def get_basic_test_manager():
    # TODO: Hier einen einfachen tree manager erstellen
    d = {'tree_id': [1] * 6,
         'post_id': [1, 2, 3, 4, 5, 6],
         'parent_id': [None, 1, 2, 3, 1, 5],
         'author_id': [1, 2, 1, 2, 3, 1],
         'in_reply_to_user_id': [None, 1, 2, 1, 1, 3],
         'text': ["I am James", "Hi James.I am Mark.", "Hi Mark", " Nice to meet you", "Hi James. I am John.",
                  "Hi John"],
         "created_at": [pd.Timestamp('2017-01-01T01'),
                        pd.Timestamp('2017-01-01T02'),
                        pd.Timestamp('2017-01-01T03'),
                        pd.Timestamp('2017-01-01T04'),
                        pd.Timestamp('2017-01-01T05'),
                        pd.Timestamp('2017-01-01T06')]}
    d2 = d.copy()
    d2["tree_id"] = [2] * 6
    d2['parent_id'] = [None, 1, 2, 3, 4, 5]
    d2['author_id'] = [1, 2, 1, 2, 1, 2]
    d2['in_reply_to_user_id'] = [None, 1, 2, 1, 2, 1]
    # Ohne dialog
    d3 = {}
    d3["tree_id"] = [3] * 4
    d3['parent_id'] = [None, 1, 1, 1]
    d3['author_id'] = [1, 2, 3, 4]
    d3['in_reply_to_user_id'] = [None, 1, 1, 1]
    d3['text'] = ["I am James", "Hi James.I am Mark.", "Hi Mark", " Nice to meet you"]
    d3['created_at'] = [pd.Timestamp('2017-01-01T01'),
                        pd.Timestamp('2017-01-01T02'),
                        pd.Timestamp('2017-01-01T03'),
                        pd.Timestamp('2017-01-01T04')]
    # a case where an author answers himself
    d4 = d3.copy()
    d4["tree_id"] = [4] * 4
    d4["author_id"] = [1, 1, 1, 2]
    d4['parent_id'] = [None, 1, 2, 1]
    d4['in_reply_to_user_id'] = [None, 1, 1, 1]

    d5 = d4.copy()
    d5["tree_id"] = [5] * 4
    d5['parent_id'] = [None, 1, 2, 3]
    d5["author_id"] = [1, 1, 1, 2]
    d5['in_reply_to_user_id'] = [None, 1, 1, 1]

    # not connected
    d6 = d4.copy()
    d6["tree_id"] = [6] * 4
    d6['parent_id'] = [None, 1, 42, 3]
    d6["author_id"] = [1, 50, 3, 4]
    d6["in_reply_to_user_id"] = [None, 1, 50, 3]

    # contains cycle
    d7 = d4.copy()
    d7["tree_id"] = [7] * 4
    d7['post_id'] = [1, 2, 3, 2]
    d7['parent_id'] = [None, 1, 2, 2]
    d7["author_id"] = [1, 2, 3, 4]
    d7['in_reply_to_user_id'] = [None, 1, 2, 2]

    df1 = pd.DataFrame(data=d)
    df2 = pd.DataFrame(data=d2)
    df3 = pd.DataFrame(data=d3)
    df4 = pd.DataFrame(data=d4)
    df5 = pd.DataFrame(data=d5)
    df6 = pd.DataFrame(data=d6)
    df7 = pd.DataFrame(data=d7)

    # df_list = [df1, df2, df3, df4, df5, df6, df7]
    # TODO implement tree with cycles
    df_list = [df1, df2, df3, df4, df5, df6]
    df = pd.concat(df_list, ignore_index=True)
    manager = TreeManager(df)
    return manager


def get_elaborate_test_manager():
    # TODO: Hier einen tree manager erstellen, der insb. lange author ids hat
    df = pd.DataFrame()
    tree = DelabTree(df=df)
    return tree


class TestDialogueFunctions(unittest.TestCase):
    def test_dialogue_paths(self):
        # Testet, ob in der Funktion dialogue_paths_to_df tatsächlich die paths beschriftet werden
        # unterscheidet zwischen elaborate und basic, um herauszufinden, ob es daran liegt, dass die zahlen
        # aktuell zu lang sind
        basic_manager = get_basic_test_manager()
        # elaborate_manager = get_elaborate_test_manager()

        basic_dialogue_paths = dialogue_paths_to_df(basic_manager)
        basic_paths = basic_dialogue_paths['path'].tolist()
        # elaborate_dialogue_paths = dialogue_paths_to_df(elaborate_manager)
        # elaborate_paths = elaborate_dialogue_paths['path'].tolist()

        self.assertIn(1, basic_paths)
        # self.assertIn(1, elaborate_paths)
