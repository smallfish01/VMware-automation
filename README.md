# VMware-automation
关于VMware 自动化运维的一些小工具.<br>
Some of VMware operation tools/scripts and programs in daily work.

Version history:

1.09/10/2021: V1.0 created.<br>
2.09/18/2021: V1.2<br>
V1.2修改内容：<br>
a.增加部分注释,删除无用的调试注释信息；<br>
b.针对在启动和关闭VM时，如果VM名字输入错误则中止操作，退出；<br>
c.修改VM关闭方式，由之前的power off改为shutdown;<br>
d.当执行关机操作后，持续检测VM状态，当状态为正常后返回已关机提示；<br>
e.当关闭一个VM超过60s时提示错误并中止后续操作。<br>
