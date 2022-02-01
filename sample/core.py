from sample.get_solid import GetSolid
from loguru import logger
import hydra
from omegaconf import DictConfig, OmegaConf

logger.add("file_{time}.log", rotation="00:00")
logger.debug("That's it, beautiful and simple logging!")

class hi:
    """hiiiiii
    """
    def say_hi(self) -> str:
        """call get_solid function and return response

        :return: [response from get_solid]
        :rtype: str
        """
        rep = GetSolid().get_solid()
        return rep


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
