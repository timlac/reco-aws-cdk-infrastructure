
# Recordix aws-cdk infrastructure   

## Improvements

- Different chapters. 
- Randomization of items smaller than complete set.
- 


# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Building the stacks

CognitoStack:

```
cdk deploy CognitoStack-dev --context env=dev
cdk deploy CognitoStack-stage --context env=stage
cdk deploy CognitoStack-prod --context env=prod
```

EmotionDataStack:

```
cdk deploy EmotionDataStack-dev --context env=dev
cdk deploy EmotionDataStack-stage --context env=stage
cdk deploy EmotionDataStack-prod --context env=prod
```

# Sampling

Some notes on the sampling strategies employed on survey creation.

The purpose of all sampling strategies is find a specific number of filenames, e.g. items to attach to a specific survey.
All sampling strategies seek to prioritize filenames that occur least frequently in previous surveys of the same project
to make sure that the number of ratings per item is evenly distributed in the long term. 

### general input parameters:

- **valence**: The emotional valence of the generated items.
  - Type: `str` or `None`
  - Possible Values:
    - `"pos"`: Only sample filenames of positive and neutral emotional valence.
    - `"neg"`: Only sample filenames of negative and neutral emotional valence.
    - `None`: Sample from all filenames.

- **balanced_sampling_enabled**: The emotional valence of the generated items.
  - Type: `bool`
  - Possible Values:
    - `True`: Use balanced sampling.
    - `False`: Use randomized sampling.

- **samples_per_survey**: How many samples to generate.
  - Type: `int`
  - Possible values:
    - Min: 1
    - Max: dataset size

## Balanced filename sampling

The purpose of balanced filename sampling is to generate a specific number of filenames with a balanced distribution of 
emotion ids. 

input parameters:

- **emotions_per_survey**: How many emotions should be included in each survey.
  - Type: `int`
  - Possible Values:
    - `"min"`: 1
    - `"max"`: Number of emotions in the dataset


### Algorithm 

Here follows a general description of the algorithm for balanced sampling.

1. Generate `frequency2filename` dict with keys `frequency` (of previous occurrence) and values `filenames` (list of filenames).
2. Check if `emotions_per_survey` is less than the total number of emotions present in dataset. If so:
   - Select x=`emotions_per_survey` number of emotions from the lowest frequencies.
3. Calculate the distribution of emotion ids in the full dataset (or selected subset of emotions/valence). 
4. Collect a number of samples from each emotion (prioritizing the lowest frequencies in `frequency2filename`) such that 
the distribution of these sampels is approximately the same as the general distribution.
   - Note: this is subject to rounding errors when the proportion are rounded to a discrete number of samples.
5. Check if we need more samples.
6. Fill up with one of each emotion.
   - Stop when we have enough samples, e.g. the number of samples corresponding to `samples_per_survey`. 

## Randomized filename sampling

### Algorith
1. Generate `frequency2filename` dict with keys `frequency` (of previous occurrence) and values `filenames` (list of filenames).
2. Take all filenames from the lowest frequency
3. Shuffle
4. Add filenames to return list until either:
   - the number specified in `samples_per_survey` is reached.
   - the filenames at current frequency runs out, if so
     - Take all filenames at the next frequency and restart at 3. 