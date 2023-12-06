# Filename: match_pattern_inc_exc.py
"""
Provides a function for matching a string according to including and excluding regexp.

patterns in inc_patterns should be AND, but order-less
patterns in exc_patterns should be OR, order-less

"""
# Author: Da Zhang
# Created: Fri Jun  5 13:53:29 2015

import re


def match_pattern_inc_exc(name, inc_patterns, exc_patterns, verbose = False):
    """Check if the name includes all patterns in inc_patterns and non in the exc_patterns

    :param name: the name to test against
    :param inc_patterns: a string containing regexp patterns (separated by ";") for inclusion check
    :param exc_patterns: a string containing regexp patterns (separated by ";") for exclusion check
    :param verbose: whether being verbose
    :returns: match_flag, matching or not
    :rtype: boolean

    """
    
    match_flag = False
    if not inc_patterns:
        raise(ValueError, "inc_patterns cannot be empty")
    inc_patterns = inc_patterns.split(';')
    if exc_patterns:
        exc_patterns = exc_patterns.split(';')
        exc_flag = False
        inc_flag = True
        for inc_p in inc_patterns:
            inc_regex = re.compile(inc_p, re.IGNORECASE)
            for exc_p in exc_patterns:
                if not exc_p:
                    break
                exc_regex = re.compile(exc_p, re.IGNORECASE)
                if exc_regex.search(name):
                    exc_flag = True
                    break
            if inc_regex.search(name):
                inc_flag = inc_flag and True
            else:
                inc_flag = inc_flag and False
        if inc_flag and (not exc_flag):
            match_flag = True
        else:
            match_flag = False
            
        if verbose:
            if match_flag:
                msg_str = "%s DOES contain %s and does NOT contain the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
            else:
                if (not inc_flag):
                    msg_str = "SINGLE REASON: %s does NOT contain the included patterns %s, MATCH = %s" % (name, inc_patterns, match_flag)
                    if exc_flag:
                        msg_str = "DOUBLE REASON: %s does NOT contain the included patterns %s, AND DOES contain the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
                else:
                    msg_str = "SINGLE REASON: %s DOES contain included patterns %s, BUT ALSO contains the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
                    
            print(msg_str)
    else:
        inc_flag = True
        for inc_p in inc_patterns:
            inc_regex = re.compile(inc_p, re.IGNORECASE)
            if inc_regex.search(name):
                inc_flag = inc_flag and True
            else:
                inc_flag = inc_flag and False

        if inc_flag:
            match_flag = True
            
        if verbose:
            if match_flag:
                msg_str = "There are no exclusion patterns, and %s DOES contain %s, MATCH = %s" % (name, inc_patterns, match_flag)
            else:
                msg_str = "SINGLE REASON: there are no exclusion patterns, but %s does NOT contain %s, MATCH = %s" % (name, inc_patterns, match_flag)
            print(msg_str)

    return match_flag

def extract_pattern_inc_exc(name, inc_patterns, exc_patterns, bool_verbose=False, bool_debug=False):
    """Check if the name includes all patterns in inc_patterns and non in the exc_patterns, then extract the part that match the inc patterns

    :param name: the name to test against
    :param inc_patterns: a string containing regexp patterns (separated by ";") for inclusion check
    :param exc_patterns: a string containing regexp patterns (separated by ";") for exclusion check
    :param verbose: whether being verbose
    :returns: match_str, remain_str
    :rtype: None or str, str

    """
  
    if bool_debug:
        print("------------ DEBUG INFO from extract_pattern_inc_exc() starts here ------------")
  
    match_flag = False

    if not inc_patterns:
        raise(ValueError, "inc_patterns cannot be empty")
    inc_patterns = inc_patterns.split(';')

    if exc_patterns:
        exc_patterns = exc_patterns.split(';')
        exc_flag = False
        inc_flag = True

        match_start_list = []
        match_end_list = []

        for inc_p in inc_patterns:
            inc_regex = re.compile(inc_p, re.IGNORECASE)
            for exc_p in exc_patterns:
                if not exc_p:
                    break
                exc_regex = re.compile(exc_p, re.IGNORECASE)
                if exc_regex.search(name):
                    exc_flag = True
                    break
            m = inc_regex.search(name)
            if m:
                inc_flag = inc_flag and True
                match_start_list.append(m.start())
                match_end_list.append(m.end())
            else:
                inc_flag = inc_flag and False
        if inc_flag and (not exc_flag):
            match_flag = True
            match_str = name[min(match_start_list):max(match_end_list)]
            remain_str = name[0:min(match_start_list)]+name[max(match_end_list):]
        else:
            match_flag = False
            match_str = None
            remain_str = name
        if bool_debug:
            if match_flag:
                msg_str = "%s DOES contain %s and does NOT contain the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
            else:
                if (not inc_flag):
                    msg_str = "SINGLE REASON: %s does NOT contain the included patterns %s, MATCH = %s" % (name, inc_patterns, match_flag)
                    if exc_flag:
                        msg_str = "DOUBLE REASON: %s does NOT contain the included patterns %s, AND DOES contain the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
                else:
                    msg_str = "SINGLE REASON: %s DOES contain included patterns %s, BUT ALSO contains the excluded patterns %s, MATCH = %s" % (name, inc_patterns, exc_patterns, match_flag)
                    
            print(msg_str)
    else:
        inc_flag = True
        match_start_list = []
        match_end_list = []
        for inc_p in inc_patterns:
            inc_regex = re.compile(inc_p, re.IGNORECASE)
            m = inc_regex.search(name)
            if m:
                if bool_verbose:
                    print("match result for pattern ", inc_p, ": ", m.group(0))
                inc_flag = inc_flag and True
                match_start_list.append(m.start())
                match_end_list.append(m.end())
            else:
                inc_flag = inc_flag and False

        if inc_flag:
            match_flag = True
            match_str = name[min(match_start_list):max(match_end_list)]
            remain_str = name[0:min(match_start_list)]+name[max(match_end_list):]
        else:
            match_flag = False
            match_str = None
            remain_str = name

        if bool_debug:
            if match_flag:
                msg_str = "There are no exclusion patterns, and %s DOES contain %s, MATCH = %s" % (name, inc_patterns, match_flag)
            else:
                msg_str = "SINGLE REASON: there are no exclusion patterns, but %s does NOT contain %s, MATCH = %s" % (name, inc_patterns, match_flag)
            print(msg_str)

    if bool_debug:
        print("------------ DEBUG INFO from extract_pattern_inc_exc() ends here ------------\n")

    return match_str, remain_str


# # unit test
# if 0:
#     name = "1.1 C-HEAD DUAL ENERGY WO MARS"
#     inc = r'\bC[^a-zA-Z]?-'
#     exc = r'\+'
#     match_str, remain_str = extract_pattern_inc_exc(name, inc, exc, bool_verbose=True, bool_debug=True)
#     print(match_str)
#     print(remain_str)
