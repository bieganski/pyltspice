#!/usr/bin/env python3

import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def run_shell(cmd: str) -> tuple[str, str]:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    stdout, stderr = process.communicate()
    if (ecode := process.returncode):
        raise ValueError(f"Command <{cmd}> exited with {ecode}")
    return stdout, stderr


def main():
    def callback_function(raw_file, log_file):
        print("Handling the simulation data of %s, log file %s" % (raw_file, log_file))
        print((raw_file, log_file))

    # from spicelib.sim.sim_runner import SimRunner as SimRunnerBase
    # from spicelib.sim.simulator import Simulator
    from PyLTSpice.sim.sim_runner import SimRunner
    from PyLTSpice.editor.spice_editor import SpiceEditor

    script_dir = Path(__file__).parent
    test_dir = script_dir / "temp"
    netlist_file = script_dir / "testfile.net"
    LTC = SimRunner(output_folder=test_dir)
    SE = SpiceEditor(netlist_file)
    #, parallel_sims=1)
    # tstart = 0
    # for tstop in [2]: # (2, 5, 8, 10):
    #     tduration = tstop - tstart
    #     SE.add_instruction(".tran {}".format(tduration), )
    #     if tstart != 0:
    #         SE.add_instruction(".loadbias {}".format(bias_file))
    #         # Put here your parameter modifications
    #         # LTC.set_parameters(param1=1, param2=2, param3=3)
    #     bias_file = test_dir / f"sim_loadbias_{tstop}.txt"
    #     SE.add_instruction(".savebias {} internal time={}".format(bias_file, tduration))
    #     tstart = tstop
    #     print("before LTC.run")
    LTC.run(SE, callback=callback_function)

if __name__ == "__main__":
    main()