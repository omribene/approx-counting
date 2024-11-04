# approx-counting
The provided python3 code, in the file `approx-counting-patterns.py`, completes the computer-assisted proof of the main result (Theorem 1.1) in our paper. The code enumerates over a variety of parameter and technique choices in order to find a way to "fix" monotone quantities in order to apply Birgé  approximation on each of these quantities.

## Usage 
The main function is `run_main_code`. It receives several parameters, most importantly:
- `patterns`: A set of patterns (of a given length) to try the enumeration on. For the code to work as intended, please use patterns which are all of the same length (e.g., only 5-patterns).
- `try_horizontal_separator`: Whether we want to use the horizontal separator technique. For length 4 (and below) patterns it is not required, while for length 5 this technique is required.
- `try_sub_separator` and `try_horizontal_sub_separator` are two parameters related to sub-separator, a primitive which we ended up not requiring to prove the main result. These are separators that are placed after we fix a first element in the algorithm.

The last part of the code (starting with setting the value of `pattern_length`) is a typical usage example for the main function. In order to show the efficacy of our algorithm, it suffices to split the patterns into symmetry groups (where each group is closed under horizontal or vertical reflection) and test just one representative pattern from each group. The number of groups is 8 for 4-patterns (i.e., the 24=4! patterns split into 8 symmetry groups in total) and 32 for 5-patterns, for example.

In our example, we ran the main code on these represenatives. For length-4 patterns, we didn't need any of the optional flags. For length 5, we set `try_horizontal_separator = True`.
The `.txt` files contain the outputs for length 4, 5, and 6. (For 6 we also used sub-separator.)

## Remark
Notably, for length 5 there were a few pattern-separator combinations that supposedly failed:

`
1|3524, horizontal below2 ---> FAILED
1|4253, horizontal below2 ---> FAILED
`

(`horizontal below2` means that the horizontal separator was located above the value 1 and below the value 2.)

Both of these cases are easily reducible to approximate counting of 4-patterns, see the paper for more detail. That is, it is not our algorithm which failed, just the specific set of techniques employed in this particular enumeration.

The actual algorithm for these two cases is along the following lines: Counting "1"s which are to the left and bottom of the separator in each window is trivial. The rest of the sequence (e.g., 3524 / 4253) is order-isomorphic to 2413 (or 3142). The algorithm in this case does the following: for each relevant window (see the paper), we count "1"s on the bottom-left side of the separator wrt this window, and approximately count the 2413 (or 3142) in the top-right side. We then multiply these quantities to get the approximate count of 13524 (or 14253) copies in this window.
