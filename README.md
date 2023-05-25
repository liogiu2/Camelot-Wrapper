# Camelot-Wrapper
 
Camelot-Wrapper is part of the PhD thesis of [Giulio Mori](https://github.com/liogiu2) that has the objective of making an layer of communication between Experience Managers and Environments. The main project is called [EM-Glue](https://github.com/liogiu2/EM-Glue).
The aim of this library is to give a structure to [Camelot](http://cs.uky.edu/~sgware/projects/camelot/) where AIs can reason on without implementing all the camelot commands hard coded in the code. It uses [PDDL](https://planning.wiki/) as language to build a state of the word and as a medium to move informations of what is changing on the environment. 

# New release is about to come out. This page is under manteinance.
![work in progress](https://icambrogiolorenzetti.edu.it/wp-content/uploads/sites/91/Work-in-progress-1024x603-1.png?x67262)

## Compatible version of camelot tested
[Camelot v1.1](http://cs.uky.edu/~sgware/projects/camelot/v1-1/): Works both on Windows and MacOS

[Camelot v1.2](http://cs.uky.edu/~sgware/projects/camelot/v1-2/): Works only on Windows

## Project Status
The project is actively under developement. Once all the major components will be ready there will be a release. 

## Documentation
The documentation is under construction. 

## Installation
Install the latest version of the [YarnSpinner-Console](https://github.com/YarnSpinnerTool/YarnSpinner-Console) program ```ysc```. This will be used by the conversation manager to compile the ```.yarn``` files containing the conversation files. On Windows, once you downloaded the ysc program into your PC, make sure that the ```ysc.exe``` is in the path variable and accessible by the terminal. 
Then install the [YarnRunner-Python](https://github.com/relaypro-open/YarnRunner-Python)
```
pip install git+https://github.com/relaypro-open/YarnRunner-Python@v0.2.1#egg=yarnrunner_python
pip install protobuf==3.20.0
```

To have it working correcly, a Camelot Wrapper needs to be launched in combination with the [EM-Glue](https://github.com/liogiu2/EM-Glue) platform. Please check the README of that repository to successfully launch this software.

## Usage
Please contact [Giulio Mori](https://github.com/liogiu2) for any questions about how is it used.
If you use this software and you're writing a research paper, please cite our research paper where we showcase this software using the Github function for citation. 

## Table of Compatibility
### Initialization - additional_data field
| Key           | Format              | Additional information    |
|---------------|---------------------|---------------------------|
| "encounters"  | list of dictionary  | Each dictionary has 4 keys "name", "description", "metadata", "preconditions" <p> "name": string, indicates the name of the encounter. The EM will send this name to have an encounter executed. <p>"description": string, description of the encounter that the author defined.<p>"metadata": dictionary, with key "target-model" containing a list of the features that the author has defined as target for the encounter <p>"preconditions": string, a list of preconditions using PDDL   |

### Normal Communication - EM -> ENV
| Message accepted | Format              | Additional information    |
|------------------|---------------------|---------------------------|
| PDDL actions     | string              | Message containing the PDDL action to be executed |

### Normal Communication - ENV -> EM
| Key                   | Format              | Additional information                                    |
|-----------------------|---------------------|-----------------------------------------------------------|
| "new"                 | string              | New relation added to the world state                     |
| "changed_value"       | string              | Relation changed value in the world state                 |
| "new_entity"          | string              | Name of the entity that has been added to the world state |
| "update_player_model" | string              | An update to the player model happened in the environment. <p> The string contains five values formatted as: <p> "('value_1', 'value_2', [...], 'value_5')"|

## Contributing
Pull requests are welcome, but please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
