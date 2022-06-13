from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm, TourismForm, SpectrumForm
from .ml_model import logic_layer
from django.contrib import messages
# Create your views here.
res = None

def index(request):
    return render(request=request, 
                  template_name='main/index1.html')

def predict(request):
    return render(request=request, 
                  template_name='main/predict.html', context={"tourist": res})


def index3(request):
    if request.method == 'POST':
        form = TourismForm(request.POST)
        
        if form.is_valid():

            year =     form.cleaned_data['year']
            duration = form.cleaned_data['duration']
            spends = form.cleaned_data['spends'] / 1000
            mode = int(form.cleaned_data['mode'])
            purpose = int(form.cleaned_data['purpose'])
            quarter =  int(form.cleaned_data['quarter'])
            country =  int(form.cleaned_data['country'])

            x = [quarter, mode, purpose, year, duration, country, spends, 0.38]
            global res
            res = logic_layer(x)
            return redirect("/predict")
        else:
            problem = form.errors.as_data()
            # This section is used to handle invalid data 
            messages.error(request, list(list(problem.values())[0][0])[0])
            form = TourismForm()
    form = TourismForm()
    return render(request=request, template_name='main/index2.html', context={"form": form})

def index2(request):
    if request.method == 'POST':
        form = SpectrumForm(request.POST)
        
        if form.is_valid():

            timeStamp = form.cleaned_data['timeStamp']
            cell_name = form.cleaned_data["cell_name"]
            PRB_Utilisation = int(form.cleaned_data["PRB_Utilisation"])
            day_time = form.cleaned_data['day_time']
            channel_id = form.cleaned_data["channel_id"]
            interference = int(form.cleaned_data["interference"])
            signal_power = int(form.cleaned_data["signal_power"])
            channel_signal_quality = form.cleaned_data["channel_signal_quality"]
            telco = int(form.cleaned_data["telco"])

            x = [timeStamp, cell_name, PRB_Utilisation, day_time, channel_id, interference, signal_power, channel_signal_quality, telco, 0.38]
            global res
            res = logic_layer(x)
            return redirect("/predict")
        else:
            problem = form.errors.as_data()
            # This section is used to handle invalid data 
            messages.error(request, list(list(problem.values())[0][0])[0])
            form = SpectrumForm()
    form = SpectrumForm()
    return render(request=request, template_name='main/index2.html', context={"form": form})

def about(request):
    return render(request=request, 
            template_name="main/about.html")

def howtouse(request):
    return render(request=request, 
            template_name="main/howtouse.html")

def under_construction(request):
    messages.info(request, "This page coming soon..")
    return render(request=request, 
            template_name="main/under_construction.html")


from django.shortcuts import render

# Create your views here.

# from ml_trainr.models import DataSet
from .models import TrainedMLModel, DataSet
from .forms import UploadDatasetForm
from django.http import HttpResponseRedirect

import h2o
from h2o.automl import H2OAutoML


def trainml(request):
    # Generate counts of some of the main objects
    num_dataset = DataSet.objects.all().count()
    # num_ml_models = TrainedMLModel.all().count()

    # Generate form for uploading data
    if request.method == 'POST':
       
        # Get the posted form
        dset_upld_form = UploadDatasetForm(request.POST, request.FILES)
        dset_upld_form.save()  # save file.
            
    else:

        dset_upld_form = UploadDatasetForm()

    context = {
        'num_dataset': num_dataset,
        'form': dset_upld_form,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/trainml.html', context=context)


def upload(request):
    num_dataset = DataSet.objects.all().count()
    # Generate form for uploading data
    if request.method == 'POST':
        # Get the posted form
        dset_upld_form = UploadDatasetForm(request.POST, request.FILES)

        # Get handle to database
        upld_dset = DataSet()
        ml_model = TrainedMLModel()

        if dset_upld_form.is_valid():

            # Collect data from posted form
            upld_dset.name = dset_upld_form.cleaned_data['name']
            upld_dset.description = dset_upld_form.cleaned_data['description']
            upld_dset.data_file = dset_upld_form.cleaned_data['data_file']
            upld_dset.resp_colmn = dset_upld_form.cleaned_data['response_column']
            # upld_dset.upload_date = dset_upld_form.cleaned_data['upload_date']

            # Push form data to database
            upld_dset.save()
            h2o.init()

            # Import a sample binary outcome train/test set into H2O
            data_file_path = 'uploads/' + str(dset_upld_form.cleaned_data['data_file'])
            data_frame = h2o.import_file(data_file_path)

            # Identify predictors/features and response/
            x = data_frame.columns
            y = upld_dset.resp_colmn
            x.remove(y)
            train_frame, test_frame, validn_frame = data_frame.split_frame(ratios=[0.7, 0.15], seed=1)
            aml_model = H2OAutoML(max_models=20, seed=1, max_runtime_secs=600)
            aml_model.train(x=x, y=y, training_frame=train_frame)
            leadr_model = aml_model.leader
            pred_response = leadr_model.predict(test_frame)
            model_path = h2o.save_model(
                model=leadr_model, path="trained_models/", force=True)
            ml_model.model_file = str(model_path)

            ml_model.name = upld_dset.name

            ml_model.description = upld_dset.description
            ml_model.save()

    else:

        dset_upld_form = UploadDatasetForm()

    context = {
        'num_dataset': num_dataset,
        # 'num_ml_models': num_ml_models,
        'form': dset_upld_form,
    }
    # change url to ML training outcome page. locals()
    return render(request, 'main/trainml.html', context=context)

