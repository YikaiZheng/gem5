import os
import matplotlib.pyplot as plt

traffic = [round(x * 0.01, 2) for x in range(1, 51)]
latency = []
hops = []
for current in traffic:
    os.system(
        f"./build/NULL/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet --num-cpus=16 --num-dirs=16 --topology=Ring --inj-vnet=0 --vcs-per-vnet=4 --synthetic=uniform_random --sim-cycles=30000 --injectionrate={current}"
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
    latency.append(round(float(output), 3))
    print(round(float(output), 3))
    stream = os.popen(
        'grep "average_hops" m5out/stats.txt | sed "s/[^0-9]*//g"'
    )
    output = stream.read()
    if output == "":
        stream = os.popen(
            'grep "average_hops" m5out/stats.txt | grep -oP "\d*\.\d+"'
        )
        output = stream.read()
    hops.append(round(float(output), 3))

plt.figure()
plt.plot(traffic, latency, marker="o")
plt.xlabel("Injection Rate")
plt.ylabel("Latency")
plt.title("Latency-throughput curve\n (Ring, uniform_random)")
plt.savefig("3.png")

plt.figure()
plt.plot(traffic, hops, marker="o")
plt.xlabel("Injection Rate")
plt.ylabel("Hops")
plt.title("Hops-throughput curve\n (Ring, uniform_random)")
plt.savefig("4.png")
