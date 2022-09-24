def tf_human_readable(tf_coeff_list):
    order = len(tf_coeff_list)
    curr_power = order - 1
    result = ''

    for it in range(0, order):
        if tf_coeff_list[it] == 0:
            continue
        prefix = '' if tf_coeff_list[it] == 1 else tf_coeff_list[it]
        prefix = '-' if tf_coeff_list[it] == -1 else prefix
        operator = '+' if tf_coeff_list[it] > 0 else ''
        result += f'{operator} {prefix}s^{curr_power} '
        curr_power -= 1

    result = trim_trailing_symbol(result, ' ')
    result = trim_leading_symbol(result, '+')
    result = trim_leading_symbol(result, ' ')
    result = refactor_power_symbols(result, 's')
    return(result)

def trim_leading_symbol(base_string, symbol):
    result = base_string
    trim_len = len(symbol)
    if base_string[0:trim_len] == symbol:
        result = result[trim_len:]
    return result

def trim_trailing_symbol(base_string, symbol):
    result = base_string
    trim_len = len(symbol)
    if base_string[-1*trim_len:] == symbol:
        result = result[:-1*trim_len]

    return result

def refactor_power_symbols(string, variable):
    return string.replace(f'{variable}^1', f'{variable}')\
                 .replace(f'{variable}^0', '1')
