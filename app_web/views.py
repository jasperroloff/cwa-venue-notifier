import base64

from django.core.exceptions import BadRequest
from django.core.files.uploadedfile import UploadedFile

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView

from app_web.forms import UploadQRCodeForm
from app_web.tables import LocationsTable, WarningsTable
from location.models import Location, PayloadDecodeError
from location.utils import file_to_images, bytes_to_images, process_qr_code_images


class UploadQRCodeView(FormView):
    template_name = "upload.html"
    form_class = UploadQRCodeForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UploadQRCodeView, self).get_context_data(**kwargs)
        if 'locations' in kwargs.keys():
            context['table'] = LocationsTable(kwargs.get('locations'))
        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('file')

        urls = []

        for f in files:
            f: UploadedFile

            if hasattr(f.file, 'name'):
                # if files IO object has name attribute, it was saved in filesystem
                images = file_to_images(f.content_type, f.file)
            else:
                # if it hasn't, it is only saved in memory
                images = bytes_to_images(f.content_type, f.file.read())

            urls += process_qr_code_images(images)

        locations = []

        for url in urls:
            try:
                Location.get_payload_from_url(url)
                locations.append(Location.get_by_url(url))
            except PayloadDecodeError:
                continue

        return self.render_to_response(self.get_context_data(locations=locations, form=form))


class LocationDetailView(DetailView):
    template_name = "location_details.html"
    model = Location

    def get_object(self, queryset=None) -> Location:
        if 'uuid' in self.kwargs.keys():
            return Location.objects.get(uuid=self.kwargs.get('uuid'))
        elif 'url' in self.kwargs.keys():
            try:
                return Location.get_by_url(self.kwargs.get('url'))
            except PayloadDecodeError as e:
                raise BadRequest(e)

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        location: Location = context.get('object')

        check_in_records = []
        check_in_records += [w.check_in_record for w in location.tracetimeintervalwarning_set.all()]
        check_in_records += [w.check_in_record for w in location.checkinprotectedreport_set.all()]

        # prevent duplicates
        check_in_records = list(set(check_in_records))

        # sort
        check_in_records.sort(key=lambda record: record.start_interval_number, reverse=True)

        context['warnings_table'] = WarningsTable(check_in_records)

        return context
