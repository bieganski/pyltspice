import os
from PyLTSpice import SimCommander

def processing_data(raw_file, log_file):
    print("Handling the simulation data of %s, log file %s" % (raw_file, log_file))

# Select spice model
LTC = SimCommander("./examples/testfiles/Batch_Test.asc")

# Set default arguments
LTC.set_parameters(res=0, cap=100e-6, run=0)
LTC.set_component_value('R2', '2k')
LTC.set_component_value('R1', '4k')
LTC.set_element_model('V3', "SINE(0 1 3k 0 0 0)")

# Define simulation
# LTC.add_instructions(
#     "; Simulation settings",
#     ".param run = 0"
# )
# raise ValueError(dir(LTC))
for opamp in ('AD712', 'AD820'):
    LTC.set_element_model('XU1', opamp)
    for supply_voltage in (5, 10, 15):
        LTC.set_component_value('V1', supply_voltage)
        LTC.set_component_value('V2', -supply_voltage)
        # overriding he automatic netlist naming
        
        run_netlist_file = "{}_{}_{}.net".format("LTC.circuit_radic", opamp, supply_voltage)
        LTC.run(run_filename=run_netlist_file, callback=processing_data)


LTC.reset_netlist()
LTC.add_instructions(
    "; Simulation settings",
    ".ac dec 30 10 1Meg",
    ".meas AC Gain MAX mag(V(out)) ; find the peak response and call it ""Gain""",
    ".meas AC Fcut TRIG mag(V(out))=Gain/sqrt(2) FALL=last"
)

LTC.run()
LTC.wait_completion()

# Sim Statistics
print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))