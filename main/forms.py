from email import message
from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

COUNTRY_CHOICES=[
    ('0', 'Select Country'),
    ('1', 'France'),
    ('2', 'Germany'),
    ('3', 'USA'),
    ('4', 'Netherlands'),
    ('5', 'Belgium'),
    ('6', 'Irish Republic'),
    ('7', 'Australia'),
    ('8', 'Canada'),
    ('9', 'Italy'),
    ('10', 'Spain'),
    ('11', 'Switzerland'),
    ('12', 'Norway'),
    ('13', 'Japan'),
    ('14', 'Poland'),
    ('15', 'South Africa'),
    ('16', 'Denmark'),
    ('17', 'Central & South America'),
    ('18', 'Russia'),
    ('19', 'New Zealand'),
    ('20', 'Sweden'),
    ('21', 'India'),
    ('22', 'Hong Kong'),
    ('23', 'Portugsl'),
    ('24', 'Austria'),
    ('25', 'Greece'),
    ('26', 'Israel'),
    ('27', 'Middle East'),
    ('28', 'Other Africa'),
    ('29', 'Other Western Europe'),
    ('30', 'Other Asia'),
    ('31', 'Brazil'),
    ('32', 'Eastern Europe'),
    ('33', 'United Arab Emirates'),
    ('34', 'Singapore'),
    ('35', 'Czech Republic'),
    ('36', 'Malasia'),
    ('37', 'Saudi Arabia'),
    ('38', 'Nigeria'),
    ('39', 'Finland'),
    ('40', 'South Korea'),
    ('41', 'Mexico'),
    ('42', 'China'),
    ('43', 'Hungary'),
    ('44', 'Pakistan'),
    ('45', 'Turkey'),
    ('46', 'Thailand'),
    ('47', 'Egypt'),
    ('48', 'Taiwan'),
    ('49', 'Kenya'),
    ('50', 'Kuwait'),
    ('51', 'Other Eastern Europe'),
    ('52', 'Romania')]   

QUARTER_CHOICES = [
    ('0', 'Select Quarter'),
    ('1', 'January-March'),
    ('2', 'April-June'),
    ('3', 'July-September'),
    ('4', 'October-December'),
]

PURPOSE_CHOICES = [
    ('0', 'Select Purpose'),
    ('1', 'Holiday'),
    ('2', 'VFR'),
    ('3', 'Business'),
    ('4', 'Miscellaneous'),
    ('5', 'Study')
]

MODE_CHOICES = [
    ('0', 'Select Travelling Mode'),
    ('1', 'Air'),
    ('2', 'Tunnel'),
    ('3', 'Sea')
]

TELCO_CHOICES = [
    ('1', 'MTN'),
    ('2', 'GLO'),
    ('3', 'AIRTEL'),
    ('4', 'ETISALAT')
]

class TourismForm(forms.Form):
    year = forms.IntegerField(label="Year(eg.2020)", 
                              validators=[MinValueValidator(2000, message="Year is invalid!"), 
                              MaxValueValidator(9999, message="Please provide 4 digit year!")],)
    duration = forms.IntegerField(label="Duration(days)", validators=[MinValueValidator(1, message="Duration: Minimum 1 day required!")])
    spends = forms.FloatField(label="Spends in $", validators=[MinValueValidator(0.1, message="Spends: Free m Nahi Milega!"), MaxValueValidator(150000, message="Spends shouldn't be exceed 150K $")],)
    mode = forms.CharField(label="Mode", widget=forms.Select(choices=MODE_CHOICES))
    purpose = forms.CharField(label="Purpose", widget=forms.Select(choices=PURPOSE_CHOICES))
    quarter = forms.CharField(label="Quarter", widget=forms.Select(choices=QUARTER_CHOICES), )
    country = forms.CharField(label="Country", widget=forms.Select(choices=COUNTRY_CHOICES))

class SpectrumForm(forms.Form):
    timeStamp = forms.DateTimeField(label="DateTime (2018-12-19 09:26:03.478039)",
                                    validators=[MinValueValidator(2000, message="Year is invalid!"), 
                              MaxValueValidator(9999, message="Please provide 4 digit year!")])
    cell_name = forms.CharField(label="Cell id or location data")
    PRB_Utilisation = forms.FloatField(label="logical channel statistics")
    day_time = forms.DateField(label="Channel duration (09:26:03.478039)")
    channel_id = forms.IntegerField(label="Cell ID")
    interference = forms.IntegerField(label="SINR (interference data)")
    signal_power = forms.IntegerField(label="RSRP (signal power for each channel)")
    channel_signal_quality = forms.IntegerField(label="RSRQ (Channel signal quality)")
    telco = forms.CharField(label="Telco under study", widget=forms.Select(choices=TELCO_CHOICES))
    
class UploadDatasetForm(forms.Form):

    data_file = forms.FileField(help_text='Click the Browse button above to upload your dataset')

    name = forms.CharField(
        max_length=200, help_text='Enter name of training data set (e.g. Solar iradiaton data for West Africa)')

    response_column = forms.CharField(max_length=200,
        help_text="Enter name of reponse column in data set or make sure a column in your data set is called 'response'")

    description = forms.CharField(max_length=1024, help_text='Give a brief description of data set you are uploading')
    

    # cur_time = timezone.now()
    # upload_date = forms.DateTimeField(widget=forms.HiddenInput(
    #     attrs={'value': cur_time}), input_formats=['%m/%d/%y %H:%M'])
    #upload_date.widget.attrs.update('value'=cur_time)

    
