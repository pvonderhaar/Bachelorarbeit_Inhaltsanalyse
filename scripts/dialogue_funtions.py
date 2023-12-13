from delab_trees.delab_tree import DelabTree
from delab_trees import TreeManager
from delab_trees.exceptions import NotATreeException
from delab_trees.util import get_root
import networkx as nx
import matplotlib.pyplot as plt

def get_dialogue_authors(tree):
    interaction_graph = tree.as_author_interaction_graph()
    cycles = list(nx.simple_cycles(interaction_graph))
    dialogues = [lst for lst in cycles if len(lst) == 2]
    return dialogues


def get_dialogue_paths(tree):
    cycle_authors = get_dialogue_authors(tree)
    possible_ids = []
    reply_graph = tree.as_reply_graph()
    tree_as_tree = tree.as_tree()

    tree_id = tree.conversation_id
    post_df = tree.df
    for authors in cycle_authors:
        author1 = authors[0]
        author2 = authors[1]
        con_ids1 = post_df[(post_df['author_id'] == author1) & (post_df['in_reply_to_user_id'] == author2)][
            'post_id'].tolist()
        con_ids2 = post_df[(post_df['author_id'] == author2) & (post_df['in_reply_to_user_id'] == author1)][
            'post_id'].tolist()
        possible_ids.append([con_ids1, con_ids2])

    reply_graph = tree.as_reply_graph()
    root = get_root(tree_as_tree)
    paths = []
    for node in tree_as_tree:
        if tree_as_tree.out_degree(node) == 0:  # it's a leaf
            path = list(nx.shortest_path(tree_as_tree, root, node))
            paths.append(list(path))

    dialogue_paths = []
    for path in paths:
        for ids in possible_ids:
            intersection1 = set(path) & set(ids[0])
            intersection2 = set(path) & set(ids[1])
            # der Dialog soll mindetens aba sein
            if ((len(intersection1) > 1) & (len(intersection2) > 2)) | (
                    (len(intersection1) > 2) & (len(intersection2) > 1)):
                dialogue_paths.append(path)

    return dialogue_paths


def dialogue_paths_to_csv(manager):
    trees = manager.trees
    dialogue_paths_dict = {}
    for tree in trees.values():
        try:
            dialogue_paths = get_dialogue_paths(tree)
            if dialogue_paths:
                dialogue_paths_dict[tree.conversation_id] = dialogue_paths
        except NotATreeException:
            continue
    dialogue_df = tree.df
    dialogue_df['path'] = None
    dialogue_df['a/b author'] = 'x'
    for conversation_id in dialogue_paths_dict.keys():
        paths = dialogue_paths_dict[conversation_id]
        this_conversation = dialogue_df[dialogue_df['tree_id'] == conversation_id]
        # post_list = this_conversation['post_id'].tolist()
        for post_row in this_conversation.iterrows():
            post_id = post_row['post_id']
            matching_indices = [index for index, lst in enumerate(paths) if post_id in lst]
            print(matching_indices)
            post_row['path'] = matching_indices

    return dialogue_df