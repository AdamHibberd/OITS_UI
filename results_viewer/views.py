from django.conf import settings
from django.http import HttpResponse
from pathlib import Path
from zipfile import ZipFile
import os



# Create your views here.
def get_paths(request, uid):

    home = str(Path.home())
    filename = uid + '.zip'
    zip_results = os.path.join(settings.MEDIA_ROOT.replace('~',home), filename)

    zip_results=ZipFile(zip_results)

    results_by_body = {}

    intermediate_point_index = 1

    for file_name in zip_results.namelist():
        if not 'orbparam' in file_name:

            contents = zip_results.read(file_name).decode("utf-8").split('\n')

            if len(contents) > 0:
                suffix = file_name.replace(uid, '')
                suffix = suffix.replace('.txt', '')

                if suffix:
                    body = contents[0]
                else:
                    body = 'PROBE'

                # append intermediate points with an index
                if 'INTERMEDIATE POINT' in body:
                    body = body + ' ' + str(intermediate_point_index)
                    intermediate_point_index += 1

                if body in results_by_body:
                    contents_by_time = results_by_body[body]
                else:
                    contents_by_time = {}

                contents_by_time = get_contents_by_time(contents_by_time, contents)

                results_by_body[body] = contents_by_time


    results = []
    for body in results_by_body:
        # Add header
        results.append(body)
        data = results_by_body[body]
        for t in sorted(data):
            results.append(data[t])




    response = '\n'.join(results)
    return HttpResponse(response, content_type='text/plain')



def get_contents_by_time(contents_by_time, contents):

    for r in contents:

        data = r.split(',')
        if len(data) > 1:


            time = data[0].strip()

            output_row = ",".join([
                time,
                data[3],
                data[4],
                data[5],
            ])

            contents_by_time[float(time)] = output_row

    return contents_by_time
