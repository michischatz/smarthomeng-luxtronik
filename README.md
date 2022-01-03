# smarthomeng-luxtronik
Plugin for [SmartHomeNG](https://github.com/smarthomeNG/smarthome).
This plugin reads data from a headpump with a Luxtronik 2 / 2.1 controller.

## Usage
Install and activate the plugin.

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
