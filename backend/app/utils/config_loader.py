# -*- coding: utf-8 -*-
"""Config manager."""
from loguru import logger
import os
from pathlib import Path
from typing import Type
import yaml
from box import Box
from pathlib import Path
from box import Box
from pathlib import Path
from typing import TextIO

class CustomYamlLoader(yaml.FullLoader):
    """
    Add a custom constructor "!include" to the YAML loader.

    "!include" allows to read parameters in another YAML file as if it was
    the main one.
    Examples:
        To read the parameters listed in credentials.yml and assign them to
        credentials in logging.yml:
        ``credentials: !include credentials.yml``
        To call: config.credentials
    """

    def __init__(
        self,
        stream: TextIO,
    ) -> None:
        self._root = Path(stream.name).parents[0]
        super().__init__(stream)
        self.add_constructors_and_resolvers()

    def include(
        self,
        node: yaml.nodes.ScalarNode,
    ) -> Box:
        """Read yaml files as Box objects and overwrite user specific files
        Example: !include model.yml, will be overwritten by model.$USER.yml
        """
        filename = self._root / str(self.construct_scalar(node))
        return read_config(
            filename,
            loader=CustomYamlLoader,
        )

    @classmethod
    def add_constructors_and_resolvers(cls) -> None:
        """Add custom constructors and resolvers to the loader."""
        cls.add_constructor(
            "!include",
            cls.include,
        )
        # allow to use ${ENV_VARIABLE} to use environment variable in YAML read
        path_matcher = re.compile(r".*\$\{([^}^{]+)}.*")
        cls.add_implicit_resolver(
            "!path",
            path_matcher,
            None,
        )
        cls.add_constructor(
            "!path",
            _path_constructor,
        )


def _path_constructor(
    _loader: yaml.FullLoader,
    node: yaml.nodes.ScalarNode,
) -> str:
    rtn = os.path.expandvars(node.value)
    if rtn == node.value:
        raise ValueError(f"OS key {node.value} was expected, but not set.")
    return rtn


class Config:
    """App config."""

    def __init__(
        self,
        config_path: Path,
    ):
        self._config_path = config_path

    def read(
        self,
        resolve: bool = True,
    ) -> Box:
        """Reads main config file."""
        if not (
            os.path.isfile(self._config_path)
            and os.access(
                self._config_path,
                os.R_OK,
            )
        ):
            raise FileNotFoundError(self._config_path)
        config = read_config(
            self._config_path,
            CustomYamlLoader,
        )
        if resolve:
            config = self.resolve(config)
        return config

    @classmethod
    def resolve(
        cls,
        config: Box,
        master: Box | None = None,
    ) -> Box:
        """Resolve the config file."""
        master = master or config
        for (
            k,
            v,
        ) in config.items():
            if isinstance(
                v,
                dict,
            ):
                config[k] = cls.resolve(
                    Box(v),
                    master=master,
                )
            if (
                isinstance(
                    v,
                    str,
                )
                and "(!" in v
            ):
                regexp = r"\(!(.*?)\)"
                config[k] = re.sub(
                    regexp,
                    lambda m: master.get(m.group(1)),
                    v,
                )
            if isinstance(
                v,
                list,
            ):
                for (
                    i,
                    el,
                ) in enumerate(v):
                    if isinstance(
                        el,
                        str,
                    ):
                        if "(!" in el:
                            regexp = r"\(!(.*?)\)"
                            config[k][i] = re.sub(
                                regexp,
                                lambda m: master.get(m.group(1)),
                                el,
                            )
                    elif isinstance(
                        el,
                        dict,
                    ):
                        config[k][i] = cls.resolve(
                            Box(el),
                            master=master,
                        )
        return config

def read_config(
    filename: Path,
    loader: Type[yaml.FullLoader],
) -> Box:
    config = _read_config(
        filename,
        loader=loader,
    )
    return config


def _read_config(
    file_path: Path,
    loader: Type[yaml.FullLoader],
) -> Box:
    """Read any yaml file as a Box object."""

    if file_path.is_file() and os.access(
        file_path,
        os.R_OK,
    ):
        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            try:
                config_dict = yaml.load(
                    f,
                    Loader=loader,
                )
            except yaml.YAMLError as exc:
                print(exc)
        return Box(
            config_dict,
            box_dots=True,
        )
    raise FileNotFoundError(file_path)