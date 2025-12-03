import os
import pickle
import pyconll
from pyconll.unit.sentence import Sentence
from pyconll.unit.token import Token


def tree_search(tree, extract):
    """Search and extract information from a pyconll Tree object.

    The search is recursive and will call the `extract` function on all
    subtrees in the tree.

    Args:
        tree: pyconll.tree.tree.Tree instance representing a (sub)tree to
              search
        extract: function that takes a pyconll.tree.tree.Tree object and
                 returns None in case this (sub)tree does not match, otherwise
                 an object that contains the extracted information from the
                 matching (sub)tree.

    Returns:
        a list of the objects returned by `extract` for all matching subtrees
        of `tree`.
    """
    results = []
    extracted_info = extract(tree)
    if extracted_info is not None:
        results.append(extracted_info)

    for child_tree in tree:
        results.extend(tree_search(child_tree, extract))

    return results


def extract_transitive(tree):
    """Extract a (predicate, subject, object) tuple for transitive clauses.

    The subject and object need to be headed by NOUN-tagged token, and the
    predicate must be tagged VERB.

    Args:
        tree: pyconll.tree.tree.Tree instance representing a (sub)tree
              to check and extract from.

    Returns:
        If `tree` is the head of a transitive clause, a tuple of
        (predicate, subject, object) pyconll.unit.token.Token instances
        representing the heads of the predicate, subject and object
        respectively. Othe[<65;20;40M[<65;20;40Mrwise None.
        """

    # The head of te current tree/subtree is a predicate
    predicate = tree.data

    # 1.  check if the predicate token is a verb
    if predicate.upos != "VERB":
        return None

    subject = None
    obj = None

    # Iterate through the children (deendents to find the subject and object
    for child_tree in tree:
        dependent_token = child_tree.data
        deprel = dependent_token.deprel

        # universal dependencies uses label "nsubj" for subjects
        # check for a noun subject
        if deprel == 'nsubj' and dependent_token.upos == "NOUN":
            subject = dependent_token

        # check for a noun object
        elif deprel == 'obj' and dependent_token.upos  == "NOUN":
            obj = dependent_token
    # if both subject and object were found here , we have a matc
    if subject and obj:
        return (predicate, subject, obj)
    else:
        return None


def find_transitive_linear(sentence):


    """Find all Noun-VERB-NOUN sequence in a sentence
     This is a rough approximation of transitive clauses with noun-headed

     subject and object in SVO languages.


        Args:

        sentence: pyconll.unit.sentence.Sentence instance.

    Returns:

        list of (predicate, subject, object) tuples, where each element is

  [<64;38;28M]      a pyconll.unit.token.Token instance.
    """
    tokens = list(sentence)
    transitive_clauses = []

    # Iterate through all posible starting potition of a 3-token sequence
    for i in range(len(tokens) - 2):
        token_a = tokens[i]
        token_b = tokens[i + 1]
        token_c = tokens[i + 2]

        # Check trough the UPOS tags
        is_noun_a = (token_a.upos == 'NOUN')

        is_verb_b = (token_b.upos == 'VERB')

        is_noun_c = (token_c.upos == 'NOUN')

        # if the sequence is a NUN-VERB-NOUN
        if is_noun_a and is_verb_b and is_noun_c:

            # Append in teh required order
            transitive_clauses.append((token_b, token_a, token_c))

    return transitive_clauses








def main():
    data_dir = "/home/dsv/robe/lis020/labs/data"
    en_pud = pyconll.load_from_file(os.path.join(
        data_dir,
        "ud-treebanks-v2.14",
        "UD_English-PUD",
        "en_pud-ud-test.conllu"))

    # Load tables of expected transitive clauses, to check your solution
    # against.
    with open(os.path.join(data_dir, "en_pud.pickle"), "rb") as f:
        true_linear_transitives, true_tree_transitives = pickle.load(f)

    # Helper function to report discrepancies between what your code
    # finds and what was expected. Return True if everything checks out,
    # otherwise return False and print an example of what was wrong.
    def check(transitives, true_transitives):
        missing = true_transitives - transitives
        extra = transitives - true_transitives
        if missing or extra:
            print("In the following sentence:")
        if missing:
            text, pred, subj, obj = list(missing)[0]
            print(text)
            print(f"  MISSING verb/subject/object: {pred} {subj} {obj}")
        if extra:
            text, pred, subj, obj = list(extra)[0]
            print(text)
            print(f"  UNEXPECTED verb/subject/object: {pred} {subj} {obj}")
        return (not missing) and (not extra)

    # Here we test the requirements for passing.
    if "find_transitive_linear" in globals():
        print("Testing find_transitive_linear...")
        linear_transitives = set()
        for sentence in en_pud:
            transitives = find_transitive_linear(sentence)
            if transitives is None:
                break
            for pred, subj, obj in transitives:
                linear_transitives.add(
                    (sentence.text, pred.form, subj.form, obj.form))
        if check(linear_transitives, true_linear_transitives):
            print("PASSED.")
        else:
            print("FAILED.")
            return
    else:
        print("FAILED. find_transitive_linear does not exist.")
        return

    # Here we test the requirements for passing with distinction.
    if "tree_search" in globals() and "extract_transitive" in globals():
        print("Testing tree_search with extract_transitive...")
        tree_transitives = set()
        for sentence in en_pud:
            tree = sentence.to_tree()
            transitives = tree_search(tree, extract_transitive)
            if transitives is None:
                break
            for pred, subj, obj in transitives:
                tree_transitives.add(
                    (sentence.text, pred.form, subj.form, obj.form))
        if check(tree_transitives, true_tree_transitives):
            print("PASSED WITH DISTINCTION.")
        else:
            print("NO DISTINCTION.")
    else:
        print("tree_search and extract_transitive do not exist.")
        print("NO DISTINCTION.")


if __name__ == '__main__':
    main()
