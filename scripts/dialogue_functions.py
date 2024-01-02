import pandas as pd
from delab_trees.exceptions import NotATreeException
from delab_trees.util import get_root
import networkx as nx


# TODO: das ganze mit as_meraged_Self_answers


def get_dialogue_authors(tree):
    """
    Gibt alle Autoren im Tree, die an einem Dialog beteiligt sind zurück
    :param tree: Aktueller Baum (von objekt DelabTree)
    :return: Alle Autoren Ids die im Baum an Dialogen beteiligt sind (Als liste von zwei-Element Listen)
    """

    interaction_graph = tree.as_author_interaction_graph()
    cycles = list(nx.simple_cycles(interaction_graph))
    dialogues = [lst for lst in cycles if len(lst) == 2]
    return dialogues


def get_dialogue_paths(tree):
    # TODO: Teilweise sind path nicht vollständig oder doppelt im datensatz

    """
    Funktion arbeitet alle Paths heraus, in denen Dialoge vorkommen und gibt sie als Liste von post_id-Listen zurück
    :param tree: Der Aktuelle Baum, indem die Dialog-Paths gelabelt werden sollen
    :return: List of Paths (as lists)
    """

    cycle_authors = get_dialogue_authors(tree)
    possible_ids = []
    tree_as_tree = tree.as_tree()
    post_df = tree.df
    for authors in cycle_authors:
        author1 = authors[0]
        author2 = authors[1]
        con_ids1 = post_df[(post_df['author_id'] == author1) & (post_df['in_reply_to_user_id'] == author2)][
            'post_id'].tolist()
        con_ids2 = post_df[(post_df['author_id'] == author2) & (post_df['in_reply_to_user_id'] == author1)][
            'post_id'].tolist()
        possible_ids.append([con_ids1, con_ids2])

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
            # der Dialog soll mindestens aba sein
            if (((len(intersection1) >= 1) & (len(intersection2) >= 1))):
                dialogue_paths.append(path)

    return dialogue_paths


def label_ab_authors(path_df, cycle_authors):
    # TODO: was wenn axxb z.B. auftritt? Root und a oft nicht richitg zugeordnet
    #
    """
    Funktion setzt im path die Autoren auf a und b, die im dialog vorkommen
    falls es mehrere dialoge im path gibt, werden sie auf c/d usw. gesetzt.
    Alle Autoren, die nicht am Dialog beteiligt sind, bekommen ein x zugewiesen
    Alle Root Posts bekommen außerdem ein 'r' zugewiesen

    :param path_df: Der aktuelle path
    :param cycle_authors: Die Autoren, die im aktuellen Beum an einem Dialog beteiligt sind
    :return: path_df mit der neuen spalte 'a/b_auhtor'
    """

    path_df['a/b_author'] = 'x'
    path_df.loc[path_df['parent_id'] == 'nan', 'a/b_author'] = 'root'  # root
    i = 0
    for authors in cycle_authors:
        are_in_path = all(author in path_df['author_id'].tolist() for author in authors)
        if not are_in_path:
            continue

        first_author = path_df.loc[path_df['author_id'] == authors[0]].iloc[0]
        second_author = path_df.loc[path_df['author_id'] == authors[1]].iloc[0]
        if first_author['created_at'] <= second_author['created_at']:
            path_df.loc[path_df['author_id'] == authors[0], 'a/b_author'] = chr(ord('a') + i)
            path_df.loc[path_df['author_id'] == authors[1], 'a/b_author'] = chr(ord('b') + i)
        else:
            path_df.loc[path_df['author_id'] == authors[0], 'a/b_author'] = chr(ord('b') + i)
            path_df.loc[path_df['author_id'] == authors[1], 'a/b_author'] = chr(ord('a') + i)

    # falls root mit a oder b üerbschrieben wurde. Aussage: root und Teil eines diologs
    mask = (path_df['parent_id'] == 'nan') & (~path_df['a/b_author'].isin(['root', 'x']))
    path_df.loc[mask, 'a/b_author'] = 'root and ' + path_df.loc[mask, 'a/b_author']

    return path_df


def is_migration_path(path_df):
    migration_words = ["Arbeitsmigration",
                       "Asylberechtigter",
                       "Asylbewerber",
                       "Asylsuchende",
                       "Asyl",
                       "Aufenthaltserlaubnis",
                       "Aufnahmegesellschaft",
                       "Ausländer",
                       "Aussiedler",
                       "Auswanderung",
                       "Einwanderung",
                       "Ausweisung",
                       "Bildungsausländer",
                       "Bildungsinländer",
                       "Bildungsmigration",
                       "Binnenmigration",
                       "Binnenvertriebene",
                       "Blaue Karte EU",
                       "Doppelte Staatsbürgerschaft",
                       "Dublin-Verfahren",
                       "Duldung",
                       "Einbürgerung",
                       "Ermessenseinbürgerung",
                       "Familiennachzug",
                       "Flucht",
                       "Flüchtling",
                       "Freiwillige Rückkehr",
                       "Gastarbeiter",
                       "Geflüchtete",
                       "Gemeinsames Europäisches Asylsystem",
                       "Genfer Flüchtlingskonvention",
                       "Gewaltmigration",
                       "Hochqualifiziert",
                       "Integration",
                       "Irreguläre Migranten",
                       "Irreguläre Migration",
                       "Irregulärer Aufentahlt",
                       "Ius sanguinis",
                       "Ius soli",
                       "Kettenmigration",
                       "Königsteiner Schlüssel",
                       "Kontingentflüchtling",
                       "Lebensstil-Migration",
                       "Mehrstaatigkeit",
                       "Menschenhandel",
                       "Migrant",
                       "Migrationshintergrund",
                       "Migration",
                       "Non-Refoulment",
                       "Optionspflicht",
                       "Pioniermigranten",
                       "Resettlement",
                       "Residenzpflicht",
                       "Rückführung",
                       "Rücknahmeabkommen",
                       "Rücküberweisung",
                       "Remittances",
                       "Rückwanderung",
                       "Saisonwanderung",
                       "Schleuser",
                       "Schleuserkriminalität",
                       "Schutzquote",
                       "Sichere Drittstaaten",
                       "Sichere Herkunftsstaaten",
                       "Sichere Herkunftsländer",
                       "Staatenlose",
                       "Staatsangehörigkeit",
                       "Staatsbürgerschaft",
                       "Subsidärer Schutz",
                       "Unbegleitete minderjährige Flüchtlinge",
                       "Verteibung",
                       "Zirkuläre Migration"]
    is_migration = any(path_df['text'].str.contains('|'.join(migration_words), case=False))
    return is_migration


def dialogue_paths_to_df(manager):
    """
    Benutzt alle oben stehenden Funktionen, um ein Df zu erstellen, das Informationen über a/b Autoren und den path gibt
    :param manager: Mehrer Trees, die nach dialogen untersucht werden soll
    :return: neuer df mit den Spalten 'path' und 'a/b_author
    """

    trees = manager.trees
    dialogue_paths_dict = {}
    for tree in trees.values():
        try:
            dialogue_paths = get_dialogue_paths(tree)
            if dialogue_paths:
                dialogue_paths_dict[tree.conversation_id] = dialogue_paths
        except NotATreeException:
            continue

    columns = ['tree_id', 'post_id', 'parent_id', 'author_id', 'in_reply_to_user_id', 'text', 'created_at', 'path',
               'a/b_author']
    dialogue_df = pd.DataFrame(columns=columns)
    for conversation_id in dialogue_paths_dict.keys():
        paths = dialogue_paths_dict[conversation_id]
        tree = trees[conversation_id]
        tree_df = tree.df
        cycle_authors = get_dialogue_authors(tree)
        i = 1
        for path in paths:
            path_df = tree_df.loc[tree_df['post_id'].isin(path)].copy()
            path_df['path'] = i
            path_df = label_ab_authors(path_df, cycle_authors)
            if is_migration_path(path_df):
                dialogue_df = pd.concat([dialogue_df, path_df], axis=0)
            i += 1

    return dialogue_df
