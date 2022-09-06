To compile the yarn file run:
```
ysc compile initial_narrative.yarn -n Output.yarnc -t Output.csv
'''

Fighter -> pm_fight
MethodActor -> pm_method
Storyteller -> pm_story
Tactician -> pm_tact
PowerGamer -> pm_power

pm_small = 1
pm_medium = 2
pm_large = 4
pm_ultra = 8

pm_type_high = 100
pm_type_low = 40

pm_Change_type_value -> adding the value