# Camelot-Wrapper
 
Camelot-Wrapper is part of the PhD thesis of [Giulio Mori](https://github.com/liogiu2) that has the objective of making an layer of communication between Experience Managers and Environments. The main project is called [EM-Glue](https://github.com/liogiu2/EM-Glue).
The aim of this library is to give a structure to [Camelot](http://cs.uky.edu/~sgware/projects/camelot/) where AIs can reason on without implementing all the camelot commands hard coded in the code. It uses [PDDL](https://planning.wiki/) as language to build a state of the word and as a medium to move informations of what is changing on the environment. 

## Compatible version of camelot tested
[Camelot v1.1](http://cs.uky.edu/~sgware/projects/camelot/v1-1/): Works both on Windows and MacOS

[Camelot v1.2](http://cs.uky.edu/~sgware/projects/camelot/v1-2/): Works only on Windows

## Project Status
The project is actively under developement. Once all the major components will be ready there will be a release. 

## Documentation
The documentation is under construction. 

## Installation
To have it working correcly, a Camelot Wrapper needs to be launched in combination with the [EM-Glue](https://github.com/liogiu2/EM-Glue) platform. Please check the README of that repository to successfully launch this software.

(For future developments) 
Install the latest version of the [YarnSpinner-Console](https://github.com/YarnSpinnerTool/YarnSpinner-Console) program ```ysc```. This will be used by the conversation manager to compile the ```.yarn``` files containing the conversation files.
Then install the [YarnRunner-Python](https://github.com/relaypro-open/YarnRunner-Python)
```
pip install git+https://github.com/relaypro-open/YarnRunner-Python@v0.2.1#egg=yarnrunner_python
```

## Usage
Please contact [Giulio Mori](https://github.com/liogiu2) for any questions about how is it used.
If you use this software and you're writing a research paper, please cite our research paper where we showcase this software using the Github function for citation. 

## Contributing
Pull requests are welcome, but please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
