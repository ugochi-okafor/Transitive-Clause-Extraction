# Transitive Clause Extraction with Universal Dependencies

This project extracts transitive clauses from syntactically annotated data using the Universal Dependencies (UD) treebanks and the `pyconll` library.

## Goal

Identify simple transitive clauses in English, first using a basic noun–verb–noun pattern, then extending to more realistic patterns using dependency labels and relaxed word-order assumptions.

## Approach

1. **Data loading**
   - Read CoNLL‑U files from UD treebanks using `pyconll`.

2. **Baseline extraction**
   - Detect sequences of NOUN–VERB–NOUN (universal POS tags) in surface order as approximate subject–verb–object clauses.

3. **To PASS this assignment with distinction**
   - Traverse the dependency tree to:
     - Find clauses where subject and object are not strictly adjacent.
     - Handle extra words (articles, adjectives, adverbs) between arguments and verbs.
     - Use dependency labels (e.g. `nsubj`, `obj`) to identify subjects and objects beyond simple NOUN–VERB–NOUN sequences.

## Files

- `extract_transitives.py` – main script for reading CoNLL‑U files and extracting clauses.
- `utils.py` (if present) – helper functions for filtering and formatting output.
- Example `.conllu` files – UD input data.

## Requirements

- Python 3.x
- `pyconll`

Install:
```python
pip install pyconll
```
## Usage
```
python3 extract_transitives.py path/to/file.conllu > output.txt
```
Output contains lines or structured records of detected transitive clauses (sentence id, token ids, surface form, and basic subject/verb/object information).

## Notes

- The project uses a simplified definition of transitivity for teaching purposes.
- Developed as part of the Introduction to Programming course at Stockholm University, and graded with distinction.
