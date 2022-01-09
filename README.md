# smarthomeng-luxtronik
This is a plugin for [SmartHomeNG](https://github.com/smarthomeNG/smarthome).
This plugin reads data from a headpump with a Luxtronik 2 / 2.1 controller.

This plugin includes the wonderful [python-luxtronik](https://github.com/Bouni/python-luxtronik) library of [Bouni](https://github.com/Bouni)

The luxtronik controller is often used by the following known manufaturers of heat pump controllers:
* Alpha Innotec
* Siemens Novelan
* Roth
* Elco
* Buderus
* Nibe
* Wolf Heiztechnik


## Usage
Install and activate the plugin.

## Configuration
Three parameters are requiered.
1. IP or hostname of the controller
2. Port, default 8889
3. query period, default 60 seconds

## Example item
Read the temperature of the forerun:
```
LWP:
    temperature:
        forerun:
            name: temperature forerun
            type: num
            luxtronik_calculations: ID_WEB_Temperatur_TVL
```
