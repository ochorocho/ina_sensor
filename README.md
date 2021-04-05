# Home Assistant INA219

`configuration.yaml` example:

```
sensor:
  - platform: ina_sensor
    device: '/dev/i2c-1'
    address: 0x40
    scan_interval: 1
```