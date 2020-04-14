from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from pathlib import Path
import datetime
import os
import json
import uuid

class OitsParams(models.Model):
    '''
    Represents a set of submitted parameters to OITS
    Parameters should be stored as JSON
    '''
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]

    NEW = 'N'
    PROCESSING = 'P'
    COMPLETE = 'C'
    STATUS_CHOICES = [
        ('N', 'New'),
        ('P', 'Processing'),
        ('C', 'Complete'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.CharField(max_length=100, default='')

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NEW,
    )

    parameters = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uid)


    def delete(self, *args, **kwargs):

        home = settings.MEDIA_ROOT.replace('~', str(Path.home()))
        os.remove(os.path.join(home, str(self.uid) + '.zip'))

        super().delete(*args, **kwargs)  # Call the "real" save() method.



    def clean(self):
        '''
        Model validation
        '''

        # Make sure text deserializes
        try:
            params = json.loads(self.parameters)
        except Exception as e:
            raise ValidationError(e)

        if not isinstance(params['trajectory_optimization'], bool):
            raise ValidationError('trajectory_optimization must be true or false')

        if not isinstance(params['Nbody'], int) or params['Nbody'] <= 1:
            raise ValidationError('Nbody must be an integer > 1')

        if not is_list_of_strings(params['ID']):
            raise ValidationError('ID must be an array of strings')

        if not isinstance(params['NIP'], int) or params['NIP'] < 0:
            raise ValidationError('NIP must be an integer >= 0')

        check_params_are_list_of_floats(params,
            ['rIP','thetaIP','thiIP','thetalb','thetaub','thilb','thiub','t0','tmin','tmax',
            'Periacon','dVcon','Perihcon'])

        check_date_string('t01', params['t01'])
        check_date_string('tmin1', params['tmin1'])
        check_date_string('tmax1', params['tmax1'])

        if not (isinstance(params['Duration'], float) or isinstance(params['Duration'], int)):
            raise ValidationError('Duration must be a float')

        if not isinstance(params['PROGRADE_ONLY'], bool):
            raise ValidationError('PROGRADE_ONLY must be true or false')

        if not isinstance(params['RENDEZVOUS'], bool):
            raise ValidationError('RENDEZVOUS must be true or false')

        if not isinstance(params['Ndata'], int) or params['Ndata'] < 1:
            raise ValidationError('Ndata must be an integer > 1')

        if not (isinstance(params['RUN_TIME'], float) or isinstance(params['RUN_TIME'], int)):
            raise ValidationError('RUN_TIME must be a number')

        if params['RUN_TIME'] > settings.MAX_RUN_TIME:
            raise ValidationError('RUN_TIME must be no longer than {0}'.format(settings.MAX_RUN_TIME))

        if not is_list_of_strings(params['BSP']):
            raise ValidationError('BSP must be an array of strings')

        for filename in params['BSP']:
            if not filename in settings.SPICE_KERNAL_FILENAMES:
                raise ValidationError('BSP must be in {0}'.format(settings.SPICE_KERNAL_FILENAMES))


def is_list_of_strings(lst):
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False

def is_list_of_floats(lst):
    if lst and isinstance(lst, list):
        return all((isinstance(elem, float) or isinstance(elem, int)) for elem in lst)
    else:
        return False

def check_params_are_list_of_floats(params, param_names):
    for name in param_names:
        if not is_list_of_floats(params[name]):
            raise ValidationError('{0} must be a list of floats'.format(name))


def check_date_string(name, value):
    try:
        datetime.datetime.strptime(value, '%Y %b %d')
    except:
        raise ValidationError('{0} must be a date string of format yyyy MMM dd'.format(name))





