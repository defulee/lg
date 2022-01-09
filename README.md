#### install 

```
curl -fsSL https://raw.githubusercontent.com/defulee/toolbox/master/install.sh | bash
```

#### useful toolset

``` text
       _
      //  __/   /)
    _(/__(_/(__//_
            _/
            /)
            `

USAGE
ftool list:       show all commands
ftool command:    execute a command(such as color、stats)
ftool update:     update ftool
ftool uninstall:  uninstall ftool
```

#### Available commands

``` text
Available commands:
------------ common -------------
color               : terminal color
format              : 1. 提取excel文件指定列转为csv文件，使用空格分隔；2. 提取 excel 指定列并在列值附带引号，列之间使用逗号分隔
histogram           : 统计数据出现频次，并以直方图显示
number              : number conversion
stats               : collect statistics of data from a file or stdin
update              : update tb

------------- java --------------
find_in_jars        : Find file in the jar files under current directory
gc                  : GC相关:显示堆中各代垃圾收集统计、显示堆中各代的内存统计
heap                : 堆对象相关:dump heap到文件、显示jvm heap中top20的对象、显示Java堆详细信息、显示在F-Queue队列等待Finalizer线程执行finalizer方法的对象
highest_cpu_threads : Find out the highest cpu consumed threads of java, and print the stack of these threads.
jargrep             : grep text in jars

------------- book --------------
book                : 查询下载小说

------------- meta --------------
meta_doc            : 自动生成模型和字典信息markdown文档
```

## 命令介绍
- update
> 更新 ftool

#### common
- color
> 显示terminal的文字彩色效果及其打印方式
```
--------------------------------------------------------------------------------------------------------------------------------------------
fg:      1m      30m     1;30m   31m     1;31m   32m     1;32m   33m     1;33m   34m     1;34m   35m     1;35m   36m     1;36m   37m     1;37m
display:  T       T       T       T       T       T       T       T       T       T       T       T       T       T       T       T       T
--------------------------------------------------------------------------------------------------------------------------------------------

usage:  echo -e "\e[[fg] tTt \e[0m"
        eg. echo -e "\e[1;31m tTt \e[0m"
        display: T
```

- histogram
> 统计数据，按照直方图显示分布
```
    11:17	2	|▇ 1.88235%
	11:18	5	|▇▇▇▇ 4.70588%
	11:19	4	|▇▇▇ 3.76471%
	11:30	1	| 0.941176%
	11:31	1	| 0.941176%
	11:32	4	|▇▇▇ 3.76471%
	11:33	1	| 0.941176%
	11:34	2	|▇ 1.88235%
	11:35	2	|▇ 1.88235%
	11:36	1	| 0.941176%
	11:01	3	|▇▇ 2.82353%
	11:02	1	| 0.941176%
	11:03	3	|▇▇ 2.82353%
	11:04	3	|▇▇ 2.82353%
	11:05	2	|▇ 1.88235%
	11:06	5	|▇▇▇▇ 4.70588%
	11:07	3	|▇▇ 2.82353%
	11:08	7	|▇▇▇▇▇▇ 6.58824%
	11:20	2	|▇ 1.88235%
	11:21	1	| 0.941176%
	11:22	3	|▇▇ 2.82353%
	11:23	1	| 0.941176%
	11:24	1	| 0.941176%
	11:25	3	|▇▇ 2.82353%
	11:26	4	|▇▇▇ 3.76471%
	11:27	3	|▇▇ 2.82353%
	11:28	3	|▇▇ 2.82353%
	11:29	1	| 0.941176%
	11:11	3	|▇▇ 2.82353%
	11:13	3	|▇▇ 2.82353%
	11:14	3	|▇▇ 2.82353%
	11:15	2	|▇ 1.88235%
	11:16	2	|▇ 1.88235%
``` 
- stats
> collect statistics of data from a file or stdin
```
Distributions:
50%	 3
75%	 6
90%	 7
95%	 8
99%	 8
99.9%	 8
99.99%	 8

Statistics:
min	 0
max	 9
average	 3.92308
sum	 51
lines	 13

Histogram:
<=p50	7 |▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 53.8462%
<=p75	3 |▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 23.0769%
<=p90	1 |▇▇▇▇▇▇▇ 7.69231%
<=p95	1 |▇▇▇▇▇▇▇ 7.69231%
<=p99	0 | 0%
<=p999	0 | 0%
<=p9999	0 | 0%
<=pmax	1 |▇▇▇▇▇▇▇ 7.69231%
```

- number
```
2 : 1010b
10: 10
16: 0xa
```

- format
	- 功能介绍
      - 1. 提取excel文件指定列转为csv文件，使用空格分隔；
      - 2. 提取 excel 指定列并在列值附带引号，列之间使用逗号分隔
	- usage:
	```
	usage: /Users/terminus/dev/github/ftool/common/tools//format -s <separator> -q <quotes> -u <usecols> -i <inputfile.xlsx> -o <outputfile.csv>
	
	e.g.
	ftool format -i /Users/terminus/Desktop/tt.xlsx -o /Users/terminus/Desktop/tt.csv  -q -s , -c 1,2 
	```


#### java
- find_in_jars
- jargrep
- gc
```
Usage: ftool gc [OPTION] pid [<interval> [<count>]]
GC相关:显示堆中各代垃圾收集统计、显示堆中各代的内存统计
Example: ftool gc -util 1234 1000 10

Options:
    -cause  ref: jstat -gccause; 垃圾收集统计（包含原因）;默认1秒, 10次;(interval=1000, count=10);
    -util   ref: jstat -gcutil; 垃圾收集统计。默认1秒, 10次;(interval=1000, count=10);
    -new    ref: jstat -gcnew; 新生代垃圾回收统计; 默认1秒, 10次;(interval=1000, count=10);
    -old    ref: jstat -gcold; 老年代垃圾回收统计; 默认1秒, 10次;(interval=1000, count=10);
    -capacity       ref: jstat -gccapacity; 显示堆中各代的空间;
    -newcapacity    ref: jstat -gcnewcapacity; 新生代内存统计
    -oldcapacity    ref: jstat -gcoldcapacity; 老年代内存统计
    -permcapacity   ref: jstat -gcpermcapacity; 打印perm区内存情况*会使程序暂停响应*;
    -metacapacity   ref: jstat -gcmetacapacity; 元数据空间统计
```

- heap
```
Usage: ftool heap [OPTION] pid [arg]
堆对象相关:dump heap到文件、显示jvm heap中top20的对象、显示Java堆详细信息、显示在F-steue队列等待Finalizer线程执行finalizer方法的对象
Example: ftool heap -dumplive 1234

Options:
    -dump       ref:jmap -dump:format=b,file=heap.bin pid 生成堆转储快照dump文件
    -dumplive   ref:jmap -dump:live,format=b,file=heap.bin pid 生成堆活动的对象快照dump文件
    -histo      ref:jmap -histo pid | sort -nr -k([arg]+1) | head -n 21;
                    jvm heap中top20的对象;0;参数：1:按实例数量排序,2:按内存占用排序，默认为1;1
    -histolive  ref:jmap -histo:live pid | sort -nr -k([arg]+1) | head -n 21;
                    jvm heap中活动的top20的对象;0;参数：1:按实例数量排序,2:按内存占用排序，默认为1;1
    -heap       ref:jmap -heap; 显示Java堆详细信息
    -clstats       ref:jmap -clstats; 打印类加载器信息
    -finalizerinfo ref:jmap -finalizerinfo; 显示在F-steue队列等待Finalizer线程执行finalizer方法的对象
```

- highest_cpu_threads
> Find out the highest cpu consumed threads of java, and print the stack of these threads.
> 

- meta_doc
```commandline
Usage: ftool meta_doc -c config_file_path
自动生成模型和字典信息markdown文档到当前文件夹下
```
