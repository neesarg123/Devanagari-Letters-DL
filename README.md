# Devanagari-Letters-DL

#### Goal
The primary goal for this project is to train a deep convolutional neural network that identifies characters of the Devanagari Script with a high level of accuracy.

### Improvement Techniques 
#### 1. Data Augmentation
- Performing basic transformations (rotations, resclaing, cropping, etc.) can help to augment the data but there is a bottleneck to this approach. 
#### 2. Add Noise to Training Images 
- Using the Fast Gradient Sign Method (FGSM) to produce noise filters, training images will be randomly applied noise to improve model generalization
- Each training class now contains 510 more images produced from perturbations formed by FGSM.

#### Current Testing Accuracy (updated 10/22): 98.77%
#### Current Testing F1 Score (updated 10/22): 98.77%
