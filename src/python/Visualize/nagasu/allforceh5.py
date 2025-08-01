import h5py
import numpy as np
import os
import ctypes
from forceh5 import *

class AllForceData:
    def __init__(self):
        self.estimate_force_num = 100000
        self.force_num = 0
        self.all_step_ForceData_position = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)
        self.all_step_ForceData_arm = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)
        self.all_step_ForceData_force = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)

    def __load_forces(self, fileName):
        if fileName != "" and fileName[len(fileName)-3:] == ".h5":
            
            with h5py.File(fileName, 'r') as h5_forces:
                keys = list(map(str, h5_forces.keys()))
                keys.remove('force_num')
                keys = list(map(int, keys))
                newlist = sorted(keys)
                for i in newlist:
                    data_group = h5_forces[str(i)]
                    f_group = data_group['forces_2d']
                    position_array = np.array(f_group['position'], dtype=np.float64)
                    arm_array = np.array(f_group['arm'], dtype=np.float64)
                    force_array = np.array(f_group['force'], dtype=np.float64)

                    num_forces = position_array.shape[1]

                    force = ForceData()
                    for i in range(num_forces):
                        f = Force()
                        f.position = position_array[:,i]
                        f.arm = arm_array[:,i]
                        f.force = force_array[:,i]
                        force.forces.append(f)
                    self.all_step_ForceData.append(force)
                

    def load(self, fn_element):
        self.__load_forces(fn_element)

    def __load_forces_from_idx(self, fileName, idx):
        if fileName != "" and fileName[len(fileName) - 3:] == ".h5":
            self.all_step_ForceData.clear()
            with h5py.File(fileName, 'r') as h5_forces:
                # idx番目のkeyを取得
                keys = list(map(str, h5_forces.keys()))
                keys.remove('force_num')
                keys = list(map(int, keys))
                newlist = sorted(keys)

                data_group = h5_forces[str(newlist[idx])]
                f_group = data_group['forces_2d']
                position_array = np.array(f_group['position'], dtype=np.float64)
                arm_array = np.array(f_group['arm'], dtype=np.float64)
                force_array = np.array(f_group['force'], dtype=np.float64)
                num_forces = position_array.shape[1]

                force = ForceData()
                for i in range(num_forces):
                    f = Force()
                    f.position = position_array[:, i]
                    f.arm = arm_array[:, i]
                    f.force = force_array[:, i]
                    force.forces.append(f)
                self.all_step_ForceData.append(force)

    def load_from_idx(self, fn_element, idx):
        self.__load_forces_from_idx(fn_element, idx)

    def __load_forces_from_idx_for_simulation(self, fileName, idx):
        #print("debug - allforceh5.py : __load_forces_from_idx_for_simulation (fileName) = ", fileName)
        ext_without_dot = os.path.splitext(fileName)[1][1:]
        if ext_without_dot == "h5":
            # print("debug - allforceh5.py : __load_forces_from_idx_for_simulation (fileName) = ", fileName)
            self.all_step_ForceData_position = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)
            self.all_step_ForceData_arm = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)
            self.all_step_ForceData_force = np.zeros((self.estimate_force_num, 2), dtype=ctypes.c_float)
            with h5py.File(fileName, 'r') as h5_forces:
                #idx番目のkeyを取得
                keys = list(map(str, h5_forces.keys()))
                keys.remove('force_num')
                keys = list(map(int, keys))
                newlist = sorted(keys)

                data_group = h5_forces[str(newlist[idx])]
                f_group = data_group['forces_2d']
                # print("debug - allforceh5.py f_group = ", f_group)
                self.all_step_ForceData_position = np.array(f_group['position'], dtype=np.float64).transpose()
                # print("debug - allforceh5.py (self.all_step_ForceData_position) = ", self.all_step_ForceData_position)
                self.all_step_ForceData_arm = np.array(f_group['arm'], dtype=np.float64).transpose()
                self.all_step_ForceData_force = np.array(f_group['force'], dtype=np.float64).transpose()
                self.force_num = np.array(f_group['position'], dtype=np.float64).transpose().shape[0]

    def load_from_idx(self, fn_element, idx):
        self.__load_forces_from_idx(fn_element, idx)

    def load_from_idx_for_simulation(self, fn_element, idx):
        self.__load_forces_from_idx_for_simulation(fn_element, idx)

def force_data_num(post_fn):
    with h5py.File(post_fn, 'r') as h5_forces:
        keys = list(map(str, h5_forces.keys()))
        keys.remove('force_num')
        keys = list(map(int, keys))
        newlist = sorted(keys)
        data_num = len(newlist)
    return data_num
