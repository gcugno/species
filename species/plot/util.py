"""
Text.
"""


def update_labels(param):
    """
    :param param:
    :type param: list

    :return:
    :rtype: list
    """

    if 'teff' in param:
        index = param.index('teff')
        param[index] = r'$T_\mathregular{eff}$ [K]'

    if 'logg' in param:
        index = param.index('logg')
        param[index] = r'$\log\,g$ [dex]'

    if 'feh' in param:
        index = param.index('feh')
        param[index] = r'Fe/H [dex]'

    if 'radius' in param:
        index = param.index('radius')
        param[index] = r'$R$ [$\mathregular{R_{Jup}}$]'

    return param


def model_name(key):
    """
    :param key:
    :type key: str

    :return:
    :rtype: str
    """

    if key == 'drift-phoenix':
        name = 'DRIFT-PHOENIX'

    return name


def quantity_unit(param):
    """
    :param param:
    :type param: list

    :return:
    :rtype: list, list
    """

    quantity = []
    unit = []

    if 'teff' in param:
        quantity.append(r'$T_\mathregular{eff}$')
        unit.append('K')

    if 'logg' in param:
        quantity.append(r'$\log\,g$')
        unit.append('dex')

    if 'feh' in param:
        quantity.append(r'[Fe/H]')
        unit.append('dex')

    if 'radius' in param:
        quantity.append(r'$R$')
        unit.append(r'$\mathregular{R_{Jup}}$')

    return quantity, unit