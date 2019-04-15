#### install 

```
curl -fsSL https://raw.githubusercontent.com/defulee/ldf/master/install.sh | bash
```

#### ldf useful toolset

``` text
       _
      //  __/   /)
    _(/__(_/(__//_
            _/
            /)
            `

USAGE
ldf list:       show all commands
ldf command:    execute a command(such as color、stats)
ldf update:     update ldf
ldf uninstall:  uninstall ldf
```

#### Available commands

``` text
------------ common -------------
color               : terminal color
number              : number conversion
stats               : collect statistics of data from a file or stdin
update              : update ldf

------------- java --------------
btrace              : start btrace debugger
highest_cpu_threads : Find out the highest cpu consumed threads of java, and print the stack of these threads.
jargrep             : grep text in jars
```