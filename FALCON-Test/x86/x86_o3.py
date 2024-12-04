# some_file.py
import sys

import m5
from m5.objects import *
from m5.util import addToPath

# caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, '/home/rahul/FALCON-Benchmark/gem5/FALCON-Test/')
sys.path.insert(
    1, "/home/rahul/FALCON-Benchmark/gem5/configs/learning_gem5/part1/"
)
from caches import *

# Basic system setup
system = System()

# Set the clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Memory mode
system.mem_mode = "timing"  # Use 'timing' for memory timing simulation
system.mem_ranges = [AddrRange("512MB")]  # Set memory size

# CPU setup
system.cpu = X86O3CPU()

# Enable tracing
# tracer = InstTracer()
# tracer.trace_file = "instruction_trace.out"
# # Enable instruction tracing
# system.cpu.trace = True
# system.cpu.trace_file = "instruction_trace.out"
# system.cpu.tracer = InstTracer(trace_file="instruction_trace.out")

# L1 Caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# L2 Cache
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# Memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Create system workbench
system.workload = SEWorkload.init_compatible(
    "tests/test-progs/hello/bin/x86/linux/hello"
)
process = Process()
process.cmd = ["tests/test-progs/hello/bin/x86/linux/hello"]
system.cpu.workload = process
system.cpu.createThreads()

# Root system
root = Root(full_system=False, system=system)

# Instantiate and run the simulation
m5.instantiate()
print("Starting simulation...")
exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
