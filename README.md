# Home Assistant INA219

`configuration.yaml` example:

```yaml
sensor:
  - platform: ina_sensor
    # Device ID: /dev/i2c-1 == 1
    device_id: 1
    address: 0x40
    scan_interval: 1
```