# TerminalHelper-Frontend
This is a private repository for managing the code used 
while developing the frontend of Terminal Helper. 

This frontend is developed with PyQt5, 
with necessary support from the qtawesome 
as the icon assets. 

The current version is aimed to be running on 
some modified Linux system, possibly on some Chinese SoCs. 
 ~~However, before the final confirmation of exact architecture of the target system, 
this software will be developed on x86 architecture. ~~ 
We can now confirm that our project should be running on the x86 and ARM based systems, 
namely the Hygon 9250 and the Kunpeng 920. Thus the compatibility under various architecture 
should be ensured. 

The target system list now includes Kylin, Deepin UOS and so on. Their base Ubuntu version can vary, 
so we need to ensure the compatibility under different native APIs and system base environment. 

Some commonly-called list presented in this project, e.g., the current process list in the Process Manager page, is implemented using QTableView. 

The dynamic performance dashboard charts on the main page, are developed using the QtChart and ChartView 
for a better Chinese character support and the antialiasing performance. 

The speedtest environment is based on the iPerf (2) backend to avoid any problem of multi-stream error. 
But as expected, this software should have the ability to test downlink speed, thus we still need to shift back to iPerf3, 
or find some other backend that is suitable for our need. 