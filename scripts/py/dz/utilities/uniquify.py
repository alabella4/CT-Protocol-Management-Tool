# Filename: uniquify.py
"""
Define a few uniquify features for sequence type iterables.

"""
# Author: Da Zhang
# Created: Fri May 15 11:14:40 2015
# Description:

def uniquify_list_simple(target_list):
    """Uniquify a list by going through it.

    :param target_list: the sequence type iterable to work on
    :returns: u, a uniquified list
    :rtype: list ([])

    """
    u = []
    for row in target_list:
        if row not in u:
            u.append(row)
    return u

def uniquify_list_count_occurrence(target_list):
    """Uniquify a list and count the occurrence of each unique element.
    :param target_list: the sequence type iterable to work on
    :returns: unique_element_dict
    :rtype: hash table
    """
    unique_element_dict = {}
    for element in target_list:
        if element not in unique_element_dict:
            unique_element_dict[element] = 1
        else:
            unique_element_dict[element] = unique_element_dict[element] + 1
    return unique_element_dict
    
