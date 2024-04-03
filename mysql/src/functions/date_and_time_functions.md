# Date and Time Functions
[MySQL :: MySQL 8.0 Reference Manual :: 14.7 Date and Time Functions](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)

### UNIX_TIMESTAMP([date])
MySQL 8.0.28以降はUNIX_TIMESTAMP()のレンジは`1970-01-01 00:00:01.000000`から`3001-01-19 03:14:07.999999`となっている[note^5]

### FROM_UNIXTIME(unix_timestamp[,format])

---
[note^5]: For MySQL 8.0.28 and later running on 64-bit platforms, the valid range of argument values for UNIX_TIMESTAMP() is '1970-01-01 00:00:01.000000' UTC to '3001-01-19 03:14:07.999999' UTC (corresponding to 32536771199.999999 seconds).
