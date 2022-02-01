import streamlit as st
import pandas as pd
import numpy as np
from loguru import logger
import hydra
from omegaconf import DictConfig, OmegaConf

logger.add("file_{time}.log", rotation="00:00")


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
