import sys

sys.path.append("../")

import streamlit as st
import pandas as pd
import numpy as np
from loguru import logger
import hydra
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from vector_visualization.VectorAnimation import VectorViewer, Axis
import streamlit.components.v1 as components


@hydra.main(config_path="./", config_name="config")
def init_cfg(cfg):
    return OmegaConf.to_yaml(cfg)


class App:
    def __init__(self) -> None:
        logger.add("./log/file_{time}.log", rotation="00:00")
        self.show_title_and_infos()
        self.input_excels()
        self.position_axis_select_box()
        if self.uploaded_files:
            self._preprocess_data()
            self.show_plot()

    def show_title_and_infos(self):
        st.title(f"3D Vector Animation")
        st.markdown(
            "github repo here :point_right: [Github](https://github.com/WangCHEN9/vector_visualization)"
        )

    def input_excels(self):
        self.uploaded_files = st.file_uploader(
            "Upload your Excel files", accept_multiple_files=True, type=["xlsx", "xls"]
        )

    def _preprocess_data(self):
        arr_list = [
            pd.read_excel(file.read()).to_numpy() for file in self.uploaded_files
        ]
        expend_arr_list = [np.expand_dims(a, axis=-1) for a in arr_list]
        self.arr_all = np.concatenate(expend_arr_list, axis=-1)
        logger.info(f"input array shape is : {self.arr_all.shape}")

    def show_plot(self):
        with st.spinner("Working on it ..."):
            v = VectorViewer(self.arr_all, position_axis=Axis.x)
            ani = v.get_ani()
            with open("./temp/myvideo.html", "w") as f:
                print(ani.to_html5_video(), file=f)

            HtmlFile = open("./temp/myvideo.html", "r")
            source_code = HtmlFile.read()
            components.html(source_code, height=900, width=900)

    def position_axis_select_box(self):
        self.pos_axis = st.selectbox(
            "Which axis you would like the Vectors be spreaded", ("X", "Y", "Z")
        )


if __name__ == "__main__":

    st.set_page_config(
        page_title="3D Vector Animation",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/WangCHEN9/vector_visualization/issues",
            "Report a bug": "https://github.com/WangCHEN9/vector_visualization/issues",
            "About": "# Time series vector visualization with streamlit !",
        },
    )

    App()
