import pytest
from pyspark.sql import Row
from pyspark.sql.types import (
    FloatType,
    IntegerType,
    ShortType,
    StringType,
    StructField,
    StructType,
)
from datetime import datetime

from nydus.core import transform_task

SAMPLE_CHANNELS = [
    Row(location_id='00000000-0000-000b-0271-c078e4408806',
        channel_id='10000000-0000-000b-0271-c078e4408807',
        some_other_col=1),
    Row(location_id='00000000-0000-000b-0271-c078e4408806',
        channel_id='10000000-0000-000b-0271-c078e4408806',
        some_other_col=1),
    Row(location_id='00000000-0000-000b-0271-c078e4408805',
        channel_id='10000000-0000-000b-0271-c078e4408805',
        some_other_col=2346),
    Row(location_id='00000000-0000-000b-0271-c078e4408804',
        channel_id='10000000-0000-000b-0271-c078e4408804',
        some_other_col=1432),
    Row(location_id='00000000-0000-000b-0271-c078e4408803',
        channel_id='10000000-0000-000b-0271-c078e4408803',
        some_other_col=7654),
]

SAMPLE_LOCATIONS = [
    Row(location_id='00000000-0000-000b-0271-c078e4408806',
        account_id='20000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        postal_code='12345',
        some_other_col=1),
    Row(location_id='00000000-0000-000b-0271-c078e4408805',
        account_id='20000000-0000-000b-0271-c078e4408805',
        tenant_id=63,
        postal_code='67890',
        some_other_col=2346),
    Row(location_id='00000000-0000-000b-0271-c078e4408804',
        account_id='20000000-0000-000b-0271-c078e4408804',
        tenant_id=62,
        postal_code='54321',
        some_other_col=1432),
    Row(location_id='00000000-0000-000b-0271-c078e4408803',
        account_id='20000000-0000-000b-0271-c078e4408803',
        tenant_id=61,
        postal_code='09876',
        some_other_col=7654),
]

SAMPLE_HOURLY_WEATHER = [
    Row(timestamp_local=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/02 00:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=72.0,
        other_dummy_property='dumb-ditty-dumber'),
    Row(timestamp_local=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/02 01:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=72.0,
        other_dummy_property='dumb-ditty-dumber'),
    Row(timestamp_local=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/02 02:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=71.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/02 03:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=71.0,
        other_dummy_property='foobarbaz'),
    Row(timestamp_local=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/03 04:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=71.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/03 05:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=73.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/03 06:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=74.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/03 07:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=75.0,
        other_dummy_property='foobarbaz'),
    Row(timestamp_local=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/04 08:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=76.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/04 09:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=73.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/04 10:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=77.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/04 11:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=76.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/05 12:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=77.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/05 13:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=76.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/05 14:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=77.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/05 15:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=76.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/06 16:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=77.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/06 17:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=66.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/06 18:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=67.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/06 19:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=66.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/07 20:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=67.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/07 21:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=66.0,
        other_dummy_property='dumb-ditty-dumb'),
    Row(timestamp_local=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/07 22:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=68.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/07 23:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=66.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/08 00:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=12.0,
        other_dummy_property='struff'),
    Row(timestamp_local=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S'),
        date_local=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S').date(),
        date=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S').date(),
        year=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S').date().year,
        month=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S').date().month,
        day=datetime.strptime('2019/07/08 06:00:00', '%Y/%m/%d %H:%M:%S').date().day,
        postal_code='12345',
        temp_f=92.0,
        other_dummy_property='struff')
]


SAMPLE_HOURLY_AMI = [
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=4,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.8,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=5,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.8,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=6,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.75,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=7,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.7,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=8,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=0.7,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=9,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=1.4,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=10,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=1.2,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=11,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=1.3,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=12,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=1.2,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=13,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=1.4,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=14,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=3.13,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=15,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=5.13,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=16,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=4.46,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=17,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=7.79,
        num_reads_missing=0,
        a_second_dummy_property='bada'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=18,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=19,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=20,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=21,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=22,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=23,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=0,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=1,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=2,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=3,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=3.11,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=4,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=3.8,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408806',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=10,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=5.2,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    # second channel for location
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=4,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=5,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=6,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-02',
        hour_utc=7,
        year=2019,
        month=7,
        day=2,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=8,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=9,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=10,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-03',
        hour_utc=11,
        year=2019,
        month=7,
        day=3,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=12,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=13,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=14,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-04',
        hour_utc=15,
        year=2019,
        month=7,
        day=4,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bljdfaif'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=16,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='fake data, fake data all day long!'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=17,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='bada'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=18,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-05',
        hour_utc=19,
        year=2019,
        month=7,
        day=5,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=20,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=21,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=22,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-06',
        hour_utc=23,
        year=2019,
        month=7,
        day=6,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=0,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=1,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=2,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=3,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=4,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=10,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=0.1,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit'),
    Row(channel_uuid='10000000-0000-000b-0271-c078e4408807',
        tenant_id=64,
        date_utc='2019-07-08',
        hour_utc=11,
        year=2019,
        month=7,
        day=8,
        time_zone='US/Eastern',
        consumption_total=200.0,
        num_reads_missing=0,
        a_second_dummy_property='falsjfit')
]

SCHEMA_HOURLY_AMI = StructType([
    StructField('channel_uuid', StringType()),
    StructField('tenant_id', IntegerType()),
    StructField('date_utc', StringType()),
    StructField('hour_utc', ShortType()),
    StructField('year', ShortType()),
    StructField('month', ShortType()),
    StructField('day', ShortType()),
    StructField('time_zone', StringType()),
    StructField('consumption_total', FloatType()),
    StructField('num_reads_missing', IntegerType()),
    StructField('a_second_dummy_property', StringType()),
])


@pytest.mark.usefixtures('spark_session', 'clean_session')
def test_model_coarse_disagg_ami(spark_session):
    spark_session \
        .createDataFrame(SAMPLE_CHANNELS) \
        .createOrReplaceTempView('channels')

    spark_session \
        .createDataFrame(SAMPLE_HOURLY_WEATHER) \
        .createOrReplaceTempView('hourly_weather')

    spark_session \
        .createDataFrame(SAMPLE_LOCATIONS) \
        .createOrReplaceTempView('locs')

    spark_session \
        .createDataFrame(SAMPLE_HOURLY_AMI, SCHEMA_HOURLY_AMI) \
        .createOrReplaceTempView('hourly_ami')

    transform_config = {
        'task': 'tasks.model_coarse_disagg_ami.task.ModelCoarseDisaggAMI',
        'script': 'task.py',
        'type': 'task',
        'kwargs': {'ami_hist_req': 3,
                   'run_date': '2019-08-01'}
    }

    output = transform_task(spark_session, {}, transform_config)

    row_count = output.count()
    assert row_count == 1

    row_1 = output.filter(output['location_id'] == '00000000-0000-000b-0271-c078e4408806').head(1)[0]

    assert row_1.tenant_id == 64
    assert row_1.account_id == '20000000-0000-000b-0271-c078e4408806'
    assert row_1.location_id == '00000000-0000-000b-0271-c078e4408806'

    assert round(row_1.total_mean_consumption, 3) == 2.825
    assert round(row_1.AO_mean_consumption, 3) == 0.8
    assert round(row_1.heat_mean_consumption, 3) == 0.115
    assert round(row_1.cool_mean_consumption, 3) == 0.154
    assert round(row_1.other_mean_consumption, 3) == 1.756
    assert round(row_1.AO_percent, 3) == 0.283
    assert round(row_1.heat_percent, 3) == 0.041
    assert round(row_1.cool_percent, 3) == 0.054
    assert round(row_1.other_percent, 3) == 0.622
    assert round(row_1.AO_scaled_percent, 3) == 0.283
    assert round(row_1.heat_scaled_percent, 3) == 0.041
    assert round(row_1.cool_scaled_percent, 3) == 0.054
    assert round(row_1.other_scaled_percent, 3) == 0.622
    assert round(row_1.scaling_factor, 3) == 1
