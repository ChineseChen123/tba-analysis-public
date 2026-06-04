# TheBlueAlliance & Statbotics Data Collection + Analysis Script

## Description

This Python script pulls historical FRC data from the TheBlueAlliance and the Statbotics APIs. After samples are randomly selected from datasets, relevant information is outputted to a text file that can be exported for further analysis, such as hypotheses tests and confidence intervals. The example script here collects data about the win rates of veteran and rookie teams in REBUILT and the accuracy of OPR and EPA predictions in the 2026 season. 

## Getting Started

### Dependencies

* Python 3
* Python `requests` module
* Python Statbotics API

### Installing

* Download from GitHub and unzip

### Executing program

```
cd src
python main.py
```

## Authors

* [ChineseChen123](https://github.com/ChineseChen123)
* [Woqh](https://github.com/Woqh)

## Version History

* 1.0 (2026-04-06)
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## References

* [TheBlueAlliance API v3](https://www.thebluealliance.com/apidocs/v3)
* [Statbotics API](https://www.statbotics.io/docs/python)
