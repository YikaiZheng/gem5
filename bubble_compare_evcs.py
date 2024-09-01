import os
import matplotlib.pyplot as plt

traffic = [round(x * 0.01, 2) for x in range(1, 81)]
traffic2 = [round(x * 0.01, 2) for x in range(1, 81)]
traffic3 = [round(x * 0.01, 2) for x in range(1, 81)]
traffic4 = [round(x * 0.01, 2) for x in range(1, 81)]
latency = []
latency2 = []
latency3 = []   
latency4 = []
reception_rate=[]
reception_rate2=[]
reception_rate3=[]
reception_rate4=[]
hops = []
hops2 = []
hops3 = []
hops4 = []
cpus = 32
min_num_bubbles = 32
for current in traffic:
    os.system(
        f"./build/NULL/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet --num-cpus={cpus} --num-dirs={cpus} --topology=Spidergon --inj-vnet=0 --vcs-per-vnet=4 --depth=1 --routing-algorithm=10 --synthetic=uniform_random --sim-cycles=100000 --garnet-deadlock-threshold=100000 --injectionrate={current} --wormhole --min-num-bubbles={min_num_bubbles} --evcs-per-vnet=0"
    )
    stream = os.popen(
        'grep "average_packet_latency" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_packet_latency" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    latency.append(round(float(output), 3))
    print(round(float(output), 3))
    stream = os.popen(
        'grep "average_hops" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_hops" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    hops.append(round(float(output), 3))
    stream = os.popen('grep "packets_received::total" m5out/stats.txt | sed "s/[^0-9]*//g"')
    packet_num=int(stream.read())
    stream = os.popen('grep "packets_injected::total" m5out/stats.txt | sed "s/[^0-9]*//g"')
    packet=int(stream.read())
    stream = os.popen('grep "simTicks" m5out/stats.txt | sed "s/[^0-9]*//g"')
    ticks = int(stream.read())
    stream = os.popen('grep "system.clk_domain.clock" m5out/stats.txt | sed "s/[^0-9]*//g"')
    tpc = int(stream.read())
    reception_rate.append(round(packet_num * tpc /ticks / cpus, 5))
    

for current in traffic2:
    os.system(
        f"./build/NULL/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet --num-cpus={cpus} --num-dirs={cpus} --topology=Spidergon --inj-vnet=0 --vcs-per-vnet=4 --depth=1 --routing-algorithm=10 --synthetic=uniform_random --sim-cycles=100000 --garnet-deadlock-threshold=100000 --injectionrate={current} --wormhole --min-num-bubbles={min_num_bubbles} --evcs-per-vnet=1"
    )
    os.system(f"echo {current} >> network_stats3.txt")
    os.system(
        f'grep "average_packet_queueing_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_queueing_latency\s*/average_packet_queueing_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_network_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_network_latency\s*/average_packet_network_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_latency\s*/average_packet_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_hops" m5out/stats.txt | sed "s/system.ruby.network.average_hops\s*/average_hops = /" >> network_stats3.txt'
    )
    stream = os.popen(
        'grep "average_packet_latency" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_packet_latency" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    latency2.append(round(float(output), 3))
    print(round(float(output), 3))
    stream = os.popen(
        'grep "average_hops" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_hops" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    hops2.append(round(float(output), 3))
    stream = os.popen('grep "packets_received::total" m5out/stats.txt | sed "s/[^0-9]*//g"')
    packet_num=int(stream.read())
    stream = os.popen('grep "simTicks" m5out/stats.txt | sed "s/[^0-9]*//g"')
    ticks = int(stream.read())
    stream = os.popen('grep "system.clk_domain.clock" m5out/stats.txt | sed "s/[^0-9]*//g"')
    tpc = int(stream.read())
    reception_rate2.append(round(packet_num * tpc /ticks / cpus, 3))

for current in traffic3:
    os.system(
        f"./build/NULL/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet --num-cpus={cpus} --num-dirs={cpus} --topology=Spidergon --inj-vnet=0 --vcs-per-vnet=4 --depth=1 --routing-algorithm=10 --synthetic=uniform_random --sim-cycles=100000 --garnet-deadlock-threshold=100000 --injectionrate={current} --wormhole --min-num-bubbles={min_num_bubbles} --evcs-per-vnet=2"
    )
    os.system(f"echo {current} >> network_stats3.txt")
    os.system(
        f'grep "average_packet_queueing_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_queueing_latency\s*/average_packet_queueing_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_network_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_network_latency\s*/average_packet_network_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_latency\s*/average_packet_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_hops" m5out/stats.txt | sed "s/system.ruby.network.average_hops\s*/average_hops = /" >> network_stats3.txt'
    )
    stream = os.popen(
        'grep "average_packet_latency" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_packet_latency" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    latency3.append(round(float(output), 3))
    print(round(float(output), 3))
    stream = os.popen(
        'grep "average_hops" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_hops" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    hops3.append(round(float(output), 3))
    stream = os.popen('grep "packets_received::total" m5out/stats.txt | sed "s/[^0-9]*//g"')
    packet_num=int(stream.read())
    stream = os.popen('grep "simTicks" m5out/stats.txt | sed "s/[^0-9]*//g"')
    ticks = int(stream.read())
    stream = os.popen('grep "system.clk_domain.clock" m5out/stats.txt | sed "s/[^0-9]*//g"')
    tpc = int(stream.read())
    reception_rate3.append(round(packet_num * tpc /ticks / cpus, 3))

for current in traffic4:
    os.system(
        f"./build/NULL/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet --num-cpus={cpus} --num-dirs={cpus} --topology=Spidergon --inj-vnet=0 --vcs-per-vnet=4 --depth=1 --routing-algorithm=10 --synthetic=uniform_random --sim-cycles=100000 --garnet-deadlock-threshold=100000 --injectionrate={current} --wormhole --min-num-bubbles={min_num_bubbles} --evcs-per-vnet=3"
    )
    os.system(f"echo {current} >> network_stats3.txt")
    os.system(
        f'grep "average_packet_queueing_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_queueing_latency\s*/average_packet_queueing_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_network_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_network_latency\s*/average_packet_network_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_packet_latency" m5out/stats.txt | sed "s/system.ruby.network.average_packet_latency\s*/average_packet_latency = /" >> network_stats3.txt'
    )
    os.system(
        f'grep "average_hops" m5out/stats.txt | sed "s/system.ruby.network.average_hops\s*/average_hops = /" >> network_stats3.txt'
    )
    stream = os.popen(
        'grep "average_packet_latency" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_packet_latency" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    latency4.append(round(float(output), 3))
    print(round(float(output), 3))  
    stream = os.popen(
        'grep "average_hops" m5out/stats.txt | grep -oP "\d*\.\d+"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_hops" m5out/stats.txt | sed "s/[^0-9]*//g"'
        )
        output = stream.read()
    hops4.append(round(float(output), 3))
    stream = os.popen('grep "packets_received::total" m5out/stats.txt | sed "s/[^0-9]*//g"')
    packet_num=int(stream.read())
    stream = os.popen('grep "simTicks" m5out/stats.txt | sed "s/[^0-9]*//g"')
    ticks = int(stream.read())
    stream = os.popen('grep "system.clk_domain.clock" m5out/stats.txt | sed "s/[^0-9]*//g"')
    tpc = int(stream.read())
    reception_rate4.append(round(packet_num * tpc /ticks / cpus, 3))


plt.figure()
plt.plot(traffic, latency, marker="o", label="EVCs_per_vnet=0")
plt.plot(traffic2, latency2, marker="+", label="EVCs_per_vnet=1")
plt.plot(traffic3, latency3, marker="x", label="EVCs_per_vnet=2")
plt.plot(traffic4, latency4, marker="*", label="EVCs_per_vnet=3")
plt.xlabel("Injection Rate")
plt.ylabel("Latency")
plt.title(
    "Latency-throughput curve for different number of escape VCs\n (4 VCs, Spidergon, Uniform Random, 32 nodes)"
)
plt.legend()
plt.savefig("10.png")

plt.figure()
plt.plot(traffic, hops, marker="o", label="EVCs_per_vnet=0")
plt.plot(traffic2, hops2, marker="+", label="EVCs_per_vnet=1")
plt.plot(traffic3, hops3, marker="x", label="EVCs_per_vnet=2")
plt.plot(traffic4, hops4, marker="*", label="EVCs_per_vnet=3")
plt.xlabel("Injection Rate")
plt.ylabel("Hops")
plt.title(
    "Hops-throughput curve for different number of escape VCs\n (4 VCs, Spidergon, Uniform Random, 32 nodes)"
)
plt.legend()
plt.savefig("11.png")

plt.figure()
plt.plot(traffic, reception_rate, marker="o", label="EVCs_per_vnet=0")
plt.plot(traffic2, reception_rate2, marker="+", label="EVCs_per_vnet=1")
plt.plot(traffic3, reception_rate3, marker="x", label="EVCs_per_vnet=2")
plt.plot(traffic4, reception_rate4, marker="*", label="EVCs_per_vnet=3")
plt.xlabel("Injection Rate")
plt.ylabel("Reception Rate")
plt.title(
    "Reception Rate curve for different number of escape VCs\n (4 VCs, Spidergon, Uniform Random, 32 nodes)"
)
plt.legend()
plt.savefig("12.png")
