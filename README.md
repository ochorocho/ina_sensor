# Home Assistant INA219

With thanks to ochorocho, the original creator.  This fork has been updated to work with Home Assistant 2022.7 and later.  Tested on 2022.10.

Adds support for the INA219 current/power/voltage sensor to Home Assistant.

`configuration.yaml` example:

```yaml
sensor:
  - platform: ina_sensor
    # Device ID: /dev/i2c-1 == 1
    device_id: 1
    address: 0x40
    scan_interval: 1
```

:warning: The constant scanning (every second in example) can spam your logs.
To disable logging of the sensor state set the following in `configuration.yaml`:

```yaml
recorder:
  exclude:
    entity_globs:
      - sensor.ina219_*
```
