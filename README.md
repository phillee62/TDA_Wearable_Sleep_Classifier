# TDA_Wearable_sleep_classifiers

This code uses scikit-learn to classify sleep based on acceleration and photoplethymography-derived heart rate from the Apple Watch. In particular, this work implements persistent homology, one of the most widely-used method in the field of Topological Data Analysis (TDA), to extract different hidden features in the heart rate and motion data across different sleep stages. The paper associated with the work will be available at the Journal of Biological Rhythms in the near future (Accepted for publication). A preprint version is avilable [here](https://www.biorxiv.org/content/10.1101/2023.10.18.562982v1.abstract). This work is based on our previous work (Walch et al., SLEEP 2019), which is is available [here](https://academic.oup.com/sleep/article/42/12/zsz180/5549536).

## Basics

This package provides Python codes for running preprocessing and sleep stage classification using the acceleration and photoplethymography-derived heart rate from the Apple Watch. However, users will need to pull the data from [here](https://alpha.physionet.org/content/sleep-accel/1.0.0/) and add it to the `data` folder to run the pre-processing step. 

### Data

- Data collected using the Apple Watch is available on PhysioNet: [link](https://alpha.physionet.org/content/sleep-accel/1.0.0/)

- The MESA dataset is available for download at the [National Sleep Research Resource](https://sleepdata.org). You will have to request access from NSRR for the data.

## Pre-processing the data

To convert the raw data into features that can be interpreted by the classifiers, you want to run `preprocessing_runner.py.` Specifically, users will need to follow these steps: 

1. Download the [data](https://alpha.physionet.org/content/sleep-accel/1.0.0/).
2. Paste the `heart_rate`, `labels`, and `motion` folders into the `data` directory in this repository, overwriting the empty folders 
3. Run `preprocessing_runner.py`. This will take in the raw data for each subject, and use it to generate features to be read in by the classifier. The saved features will get saved to the folder `outputs/features/`, with the filename corresponding to the type of feature. For instance, the activity count feature for subject 781756 will appear as `781756_count_feature.out`. 

#### Notes
- Generating all the features should take about five minutes
- The features are text files, and if you want to see what they contain, simply open them in a text editor. 
- You should see print statements that look like this: `Cropping data from subject 8692923...`
- Followed by print statements that look like this: `Getting valid epochs... Building features...`
- The preprocessing step generates three main types of features: 
    1) The magnitude of activity level based on acceleration data and standard deviation of heart rate in a given 30-seconds epoch. These features were developed and used in our original work (Walch et al., SLEEP 2019), hence we denote this as `original features`. These features can be obtained by running `RawDataProcessor.crop_all()` in `preprocessing_runner.py`.

    2) The estimation of circadian propensities on sleep stages. We propose two types of such circadian rhythms-based features using a mathematical model of human circadian pacemaker (Forger et al., J. Biol. Rhythms 1999) that was fitted to the melatonin secretion rhythms. A second approach uses a statistical model of the human circadian rhyhtms in the cardiac pacemaker (Bowman et al., Cell. Rep. Methods 2021). This feature represents the effect of human circadian rhythms in peripheral tissues (e.g., cardiac tissues, liver, kidney, etc) on the sleep drives. These features are therefore named `clock proxies`. These features can be obtained by running `CircadianService.build_circadian_model()` and `CircadianService.build_CRHR_model()`, respectively, in `preprocessing_runner.py`.

    3) The hidden features capturing the underlying deynamics in motion and heart rate across different sleep stages. These features are obtained by implementing TDA, specifically persistent homology. Broadly speaking, these features would represent the hidden periodic patterns of motion and heart rate in some high dimensional space, which is typically difficult to quantify or visualize with conventional statistical methods. We name these as `topological features`. Likewise, these features can be obtained by running `FeatureBuilder.build()` in `preprocessing_runner.py`.

    Please see `Methods` section in [link](https://www.biorxiv.org/content/10.1101/2023.10.18.562982v1.abstract) for details on the underlying methodologies used to obtain each features. 
 
## License

This software is open source and under an MIT license.
