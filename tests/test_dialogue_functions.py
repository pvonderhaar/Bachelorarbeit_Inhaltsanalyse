import unittest
from scripts.dialogue_functions import dialogue_paths_to_df
from delab_trees.delab_tree import DelabTree
import pandas as pd


def get_basic_test_manager():
    # TODO: Hier einen einfachen tree manager erstellen
    df = pd.DataFrame()
    tree = DelabTree(df=df)
    return tree


def get_elaborate_test_manager():
    # TODO: Hier einen tree manager erstellen, der insb. lange author ids hat
    df = pd.DataFrame()
    tree = DelabTree(df=df)
    return tree

class TestDialogueFunctions(unittest.TestCase):
    def test_dialogue_paths(self):
        # Testet, ob in der Funktion dialogue_paths_to_df tatsächlich die paths beschriftet werden
        # unterscheided zwischen elaborate und basic, um herauszufinden, ob es daran liegt, dass die zahlen
        # aktuell zu lang sind
        basic_manager = get_basic_test_manager()
        elaborate_manager = get_elaborate_test_manager()

        basic_dialogue_paths = dialogue_paths_to_df(basic_manager)
        basic_paths = basic_dialogue_paths['path'].tolist()
        elaborate_dialogue_paths = dialogue_paths_to_df(elaborate_manager)
        elaborate_paths = elaborate_dialogue_paths['path'].tolist()

        self.assertIn(1, basic_paths)
        self.assertIn(1, elaborate_paths)







