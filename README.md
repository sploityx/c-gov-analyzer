# C-Gov-Analyzer

## Description

The C-Gov-Analyzer tool allows for switching out the idle-governor within a system in order to test each idle-governor individually.
Testing idle-governors is not trivial, as the noise created by the kernel functions, kernel interupts and other applications result is outnumbering most suitable benchmarks.
It is using the functionallity from the out-of-tree perf-powerstat[^1] Linux Kernel Module.
Furthermore, it can utilize the corresponding post-processing module[^2] to visualize the aquired data.

[^1]: https://github.com/protocollabs/linux-kernel-perf/tree/flo/perf-powerstat
[^2]: https://github.com/hgn/perf-power-analyzer-post

## Example

For examples you can check the post-processing repository[^6].

[^6]: https://github.com/hgn/perf-power-analyzer-post/tree/flo/idle-gov-metric/idle-gov-comp/examples


## Suitable Benchmarks

You can specifiy all executable workloads on the system.
If you want to test your system with an already running load, you can just specify to sleep.
The benchmarks should be kept as minimal as possible to decrease the noise level.
To utilize a benchmark correctly, all parameters of the benchmarks need to be fitted to the SuT.
Working on soley CPU benchmarks, you should aim for a load between 10% and 80% depending on your needs.
Any higher load results in sole usage of the lowest C-State or POLL.
While with any lower load, all idle-governors frequently rely on the highest C-State.

### stress[^3]

stress allows for testing a SuT with a multitude of scenarios, most importantly io-load and cpu-load.
It can be used with multiple parameters spawning different kinds of workers, which can ideally should be specified inside a script to be executed. 

[^3]: https://github.com/resurrecting-open-source-projects/stress

### mini-bench[^4]

The mini-bench application allows for the maximum amount of sleeps over a specific time.
This benchmark sleeps for random intervals, which can be seeded.
All incoming interrupts should come from others sources, e.g. Kernel Interrupts, as this programm has none. 
Setting isol_cpus or cgroups is sufficient for this program.

[^4]: https://github.com/hgn/perf-power-analyzer-post

### io-net-cpu-bench[^5]

io-net-cpu-bench creates a mixxed workload of both mini-bench and stress.
It utilizes random sleep times after tasks, while also executing a certain workload, i.e. io, net or cpu workload.

[^5]: https://github.com/hgn/perf-power-analyzer-post

