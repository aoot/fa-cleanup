import re

def parse_fa(value):
    '''Matches an input string using various logic and returns the match as a dictionary.

    Args: 
        value (str): String to be parsed  

    Returns:
        A dict of parsed first-ascent (FA) information. 
    '''
    result = {
        'climbers': [],
        'year': None,
        'month': None,
        'day': None,
        'equipped': None,
        'needs_manual_review': None,
        'unknown_expression': False,
        'unsure': False,
    }

    ## Matching: Patterns that need manual reviews
    for word in ('unknown', 'n/a'):
        if word in value:
            result['needs_manual_review'] = True
            return result

    ## Matching: Contains a question mark >>> Needs further manual investigation of FA
    if value[-1] == '?':
        result['unsure'] = True
        value = value[:-1]

    # support here abbreviated names/last names (e.g. "m. black")
    person_name_expr = '([a-z]+ [a-z]+)'
    year_expr = '([0-9]{4})'
    date_expr = f'([0-9]+)/([0-9]+)/{year_expr}'
    
    ## Matching: Single FullName (FullName is defined by `person_name_expr`)
    match = re.search(f'^{person_name_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        return result

    ## Matching: Single year expression
    match = re.search(f'^{year_expr}$', value)
    if match:
        result['year'] = match.group(1)
        return result

    ## Matching: FullName with zero-or-one comma, followed by year
    match = re.search(f'^{person_name_expr},? {year_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        result['year'] = match.group(2)
        return result

    ## Matching: date expression
    ## NOTE: 
    ## - Assumes date sequence as Month/Day/Year
    match = re.search(f'^{person_name_expr},? {date_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        # Assumin month/day/year format
        result['month'] = match.group(2)
        result['day'] = match.group(3)
        result['year'] = match.group(4)
        return result

    ## Matching: Final catch all 
    result['unknown_expression'] = True
    return result
