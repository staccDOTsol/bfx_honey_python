setlocal enabledelayedexpansion
for %%f in (.\*.json) do (
  START /B python run_strat_demo2.py "%%~nf"
  
)
