# Problem Set 4A
# Name: Mario Castillo
# Collaborators: None
# Time Spent: From 08/12/2017 to 08/13/2017

def get_permutations(sequence):
    ''' Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

        Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'] '''

    if len(sequence) == 1:
        return [sequence]  # Base case

    perm_list = []
    for a in sequence:  # cycle though sequence to take item from sequence
        rem_elem = ''  # variable that stores reduced version of the problem
        for x in sequence:  # loop used to remove item -a- from sequence
            if x != a:
                rem_elem += x
        z = get_permutations(rem_elem)  # recursive call on reduced version of the problem

        for t in z:
            perm_list.append(a + t)  # append permuted elements to removed items
    return perm_list

if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
