import click

from . import cli


def __get_required_options(command):
    required_options = [
        param.name for param in command.params
        if isinstance(param, click.Option) and param.required
    ]
    return required_options


def __check_required_but_missing_params(_method, _kwargs):
    req = __get_required_options(_method)
    required_but_missing = [p for p in req if p not in _kwargs]

    if required_but_missing:
        missing_params = ', '.join(required_but_missing)
        raise ValueError(f'The following required arguments are missing: {missing_params}')


def __invoke(cli_method, _kwargs):
    __check_required_but_missing_params(cli_method, _kwargs)
    ctx = click.Context(cli_method)
    ctx.invoke(cli_method, **_kwargs)






def list_tools(**kwargs):
    __invoke(cli.list_tools, kwargs)

def blastn(**kwargs):
    __invoke(cli.blastn, kwargs)


def tblastn(**kwargs):
    __invoke(cli.tblastn, kwargs)





__all__ = ['blastn']