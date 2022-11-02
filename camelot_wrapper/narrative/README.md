To compile the yarn file run:
```
ysc compile initial_narrative.yarn -n Output.yarnc -t Output.csv
'''

Fighter -> pm_fight         <<update_player_model 40 0 0 0 0>>      <<update_player_model 100 0 0 0 0>>
MethodActor -> pm_method    <<update_player_model 0 40 0 0 0>>      <<update_player_model 0 100 0 0 0>>
Storyteller -> pm_story     <<update_player_model 0 0 40 0 0>>      <<update_player_model 0 0 100 0 0>>
Tactician -> pm_tact        <<update_player_model 0 0 0 40 0>>      <<update_player_model 0 0 0 100 0>>
PowerGamer -> pm_power      <<update_player_model 0 0 0 0 40>>      <<update_player_model 0 0 0 0 100>>

pm_small = 1
pm_medium = 2
pm_large = 4
pm_ultra = 8

pm_type_high = 100
pm_type_low = 40

pm_Change_type_value -> adding the value