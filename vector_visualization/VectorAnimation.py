import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import pandas as pd
from pathlib import Path
from typing import List
from loguru import logger


class QuiverForce:
    def __init__(self, arr, ax) -> None:
        self.arr = arr
        self.num_of_vector = arr.shape[-1]
        self.ax = ax
        self._init_quiver()

    def _init_quiver(self):
        self._set_ax_lim()
        self._get_quiver_positions()
        self._set_quiver(0)

    def _set_ax_lim(self, scale=2):
        self.x_min = self.arr[:, 0, :].min() * scale
        self.x_max = self.arr[:, 0, :].max() * scale

        self.y_min = self.x_min
        self.y_max = self.x_max

        self.z_min = self.arr[:, 2, :].min() * scale
        self.z_max = self.arr[:, 2, :].max() * scale

        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_zlim(self.z_min, self.z_max)

    def _get_quiver_positions(self, scale=2):
        # * scale should be 2 for in the middle
        self.pos = []
        self.pos.append([0, self.y_min / scale])
        self.pos.append([0, self.y_max / scale])
        self.pos.append([self.x_min / scale, self.y_min / scale])
        self.pos.append([self.x_max / scale, self.y_min / scale])
        self.pos.append([self.x_min / scale, self.y_max / scale])
        self.pos.append([self.x_max / scale, self.y_max / scale])

    def _get_arrow(self, row, last_axis):
        x = self.pos[last_axis][0]
        y = self.pos[last_axis][1]
        z = 0
        u = self.arr[row, 0, last_axis]
        v = self.arr[row, 1, last_axis]
        w = self.arr[row, 2, last_axis]
        output = [x, y, z, u, v, w]
        logger.debug(output)
        return output

    def _set_quiver(self, index):
        self.q0 = self.ax.quiver3D(*self._get_arrow(index, last_axis=0), color="red")
        self.q1 = self.ax.quiver3D(*self._get_arrow(index, last_axis=1), color="red")
        self.q2 = self.ax.quiver3D(*self._get_arrow(index, last_axis=2), color="blue")
        self.q3 = self.ax.quiver3D(*self._get_arrow(index, last_axis=3), color="blue")
        self.q4 = self.ax.quiver3D(*self._get_arrow(index, last_axis=4), color="blue")
        self.q5 = self.ax.quiver3D(*self._get_arrow(index, last_axis=5), color="blue")

    def _remove_all_quiver(self):
        self.q0.remove()
        self.q1.remove()
        self.q2.remove()
        self.q3.remove()
        self.q4.remove()
        self.q5.remove()

    def update(self, index):
        self._remove_all_quiver()
        self._set_quiver(index)


class VectorViewer:
    def __init__(self, arr: np.ndarray):
        """init function for vector viewer

        Args:
            arr (np.ndarray): [input array,shape = (number_of_rows,3,number_of_vector)]
        """
        self.arr = arr
        print(self.arr.shape)
        self.length = self.arr.shape[0]
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.quiver_force = QuiverForce(self.arr, ax=self.ax)

    def get_view(self):
        self.ani = FuncAnimation(
            self.fig,
            self.quiver_force.update,
            frames=range(self.length),
            interval=1,
            repeat=False,
        )
        plt.show()

    def save_ani(self, save_path: Path):
        writergif = animation.PillowWriter(fps=30)
        self.ani.save(str(save_path), writer=writergif)
        print(f"Animation saved to {save_path} !")


if __name__ == "__main__":
    # run_id = "FL201135"  # fc = 0.07
    run_id = "FL220185"  # fc = 0.1
    # run_id = "FL220186"

    folder = Path(
        f"N:\db-lms\chenwang\W33_MT30_D0324626\ZMS\MASTER\{run_id}\contact_force\merged"
    )
    files = list(folder.glob("*.xlsx"))
    arr_list = [pd.read_excel(file).to_numpy() for file in files]
    expend_arr_list = [np.expand_dims(a, axis=-1) for a in arr_list]
    arr_all = np.concatenate(expend_arr_list, axis=-1)
    print(arr_all.shape)

    save_path = folder / "force_vector_animation.gif"

    v = VectorViewer(arr_all)
    v.get_view()
    v.save_ani(save_path)
