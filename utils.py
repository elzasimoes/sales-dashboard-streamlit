class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def format_number(value, prefix=''):
        """ """

        for unidade in ['', 'mil']:
            if value < 1000:
                return f'{prefix} {value:.2f} {unidade}'

            value /= 1000
        return f'{prefix} {value:.2f} {unidade} milhões'
