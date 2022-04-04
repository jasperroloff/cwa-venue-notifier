import django_tables2

from location.models import Location
from warning.models import CheckInRecord


class LocationsTable(django_tables2.Table):
    location_id = django_tables2.Column(linkify=True)
    description = django_tables2.Column()
    address = django_tables2.Column()
    # selected = django_tables2.CheckBoxColumn(accessor='uid', checked=True, verbose_name='miau')

    def render_location_id(self, value: bytes):
        return value.hex()

    def render_uuid(self, record: Location):
        if record.pk:
            return record.uuid
        else:
            return None

    class Meta:
        model = Location
        orderable = False
        exclude = ('id', 'uuid', 'location_id_hash', 'url')


class WarningsTable(django_tables2.Table):
    date = django_tables2.DateColumn()
    start = django_tables2.TimeColumn()
    end = django_tables2.TimeColumn()
    duration = django_tables2.Column()
    transmission_risk_level = django_tables2.Column()

    def render_date(self, record: CheckInRecord):
        return record.start.date().isoformat()

    def render_start(self, record: CheckInRecord):
        return f'{record.start.time()} ({record.start.tzname()})'

    def render_end(self, record: CheckInRecord):
        return f'{record.end.time()} ({record.start.tzname()})'

    def render_duration(self, record: CheckInRecord):
        return str(record.duration)

    class Meta:
        exclude = ('id', 'type', 'start_interval_number', 'period')
        orderable = False
        model = CheckInRecord

