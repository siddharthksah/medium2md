A hitchhiker’s guide to Synthetic data for Deep Learning
========================================================

What’s synthetic data?

Synthetic data in machine learning refers to the creation of artificially generated data sets that mimic real-world data and can be used for training machine learning models. The purpose of using synthetic data is to overcome limitations in collecting and using real-world data for training, such as data privacy concerns, the unavailability of large enough data sets, or the need to artificially balance the data. Synthetic data can be generated using various methods, such as generative models, simulations, or statistical sampling techniques.

Why should we care?

Several reasons actually.

1. Overcoming data privacy concerns: In some cases, it may not be possible to use real-world data due to privacy or confidentiality issues. Synthetic data can provide a solution to this problem by generating data that resembles the real-world data but doesn’t contain any sensitive information.
2. Balancing the data: In some cases, the real-world data may be imbalanced, meaning that there is a disproportionate number of samples for certain classes. Synthetic data can be generated to balance the data and improve the performance of the machine learning model.
3. Lack of data: In some cases, there may not be enough real-world data to train a machine learning model. Synthetic data can be generated to supplement the real-world data and increase the size of the data set.
4. Testing and validation: Synthetic data can also be used to test and validate machine learning models by providing a controlled environment for experimentation.
5. Domain adaptation: When the real-world data for a particular domain is limited, synthetic data can be generated from a related domain to help train the machine learning model.

What kind of synthetic data can we really generate, though?

1. Tabular Synthetic Data: This type of synthetic data refers to artificially generated data in a tabular format, such as a spreadsheet or a database table. It is commonly used for testing machine learning algorithms and addressing class imbalance in datasets.
2. Image Synthetic Data: This type of synthetic data refers to artificially generated images, used for training machine learning models in computer vision and object detection tasks.
3. Text Synthetic Data: This type of synthetic data refers to artificially generated text, used for training machine learning models in natural language processing and text classification tasks.
4. Audio Synthetic Data: This type of synthetic data refers to artificially generated audio, used for training machine learning models in audio processing and speech recognition tasks.
5. Time Series Synthetic Data: This type of synthetic data refers to artificially generated time series data, used for training machine learning models in forecasting and time series analysis tasks.
6. Spatial Synthetic Data: This type of synthetic data refers to artificially generated spatial data, used for training machine learning models in geographic information systems and spatial analysis tasks.
7. Video Synthetic Data: This type of synthetic data refers to artificially generated video, used for training machine learning models in video processing and object detection tasks.

Let’s talk about these in not-so-much detail

1. Tabular Synthetic Data

Tabular synthetic data refers to the generation of artificial data that resembles tabular data, such as a spreadsheet or a database table, with rows and columns of data. Each row in a table of synthetic data is a sample, and each column is a feature.

Tabular synthetic data can be generated using various methods, such as statistical sampling, simulation, or machine learning models such as generative adversarial networks (GANs) or variational autoencoders (VAEs). The methods used will depend on the desired properties of the synthetic data, such as the distribution of the data, the correlation between features, or the presence of outliers or anomalies.

Tabular synthetic data can be used in various applications, such as data privacy and confidentiality, data augmentation, model testing and validation, and model deployment. By generating synthetic data that resembles real-world data, it can help overcome challenges associated with using real-world data, such as data scarcity, data imbalance, or data privacy concerns.

However, it’s important to note that while synthetic data can be a valuable tool, it can also have limitations, such as not perfectly capturing the complex relationships and patterns in real-world data. Therefore, it’s important to evaluate the quality of the synthetic data and compare it to the real-world data to ensure that it meets the desired requirements.

Main libraries in Python —

* [gretel-synthetics](https://github.com/gretelai/gretel-synthetics) — Generative models for structured and unstructured text, tabular, and multi-variate time-series data featuring differentially private learning.
* [SDV](https://github.com/sdv-dev/SDV) — Synthetic Data Generator for tabular, relational, and time series data.

Let’s build a model and make ourselves some “new” tabular data. I will be using SDV for this example.


```
# create an environment and install libraries we will need  
conda create -n synthetic\_tabular python==3.8 -y  
conda activate synthetic\_tabular  
pip install pandas\_profiling  
pip install sdv==0.13.1 -q
```
I like to check all the dependencies if they have been properly installed before running my code


```
pip show sdv  
pip show pandas\_profiling
```
Let’s load a clean tabular data for this example. We will use pandas profiling library to get insights fast.

The pandas profiling library is used to generate exploratory reports for Pandas DataFrames. It provides a fast and simple way to perform exploratory data analysis (EDA) and identify patterns, trends, and potential problems in the data.

The library generates a comprehensive report that includes information such as:

1. Overview: A summary of the DataFrame, including its shape, size, and data types.
2. Descriptive statistics: A summary of the central tendencies, dispersion, and distribution of the data.
3. Missing values: A summary of the missing values in the data, including the number and percentage of missing values for each column.
4. Correlations: A matrix showing the correlations between the columns in the data.
5. Outliers: Identification of outliers in the data using scatter plots, histograms, and box plots.
6. Duplicates: A summary of the duplicate records in the data.
7. Frequency tables: A summary of the frequency distribution of the categorical variables in the data.
8. High-cardinality variables: Identification of columns with high cardinality (a large number of unique values).


```
import warnings  
  
import pandas as pd  
from pandas\_profiling import ProfileReport  
  
from sdv.evaluation import evaluate  
from sdv.metrics.tabular import CSTest, KSTest, LogisticDetection, SVCDetection  
from sdv.tabular import CTGAN, TVAE, CopulaGAN, GaussianCopula  
  
warnings.filterwarnings("ignore")  
  
import numpy as np  
# you can download the adult.csv file from here  
# https://www.kaggle.com/datasets/uciml/adult-census-income?select=adult.csv  
real\_data = pd.read\_csv("adult.csv").replace('?',np.nan).dropna().sample(1000)  
  
print(real\_data.shape)  
real\_data.head()  
  
cat\_columns = [  
 "workclass",  
 "education",  
 'education.num'  
 "marital.status",  
 "occupation",  
 "relationship",  
 "race",  
 "sex",  
 "native.country",  
 "income",  
]
```

```
# lets do some visualization  
profile = ProfileReport(  
 real\_data, title="Profiling Real Adult Data", html={"style": {"full\_width": True}}  
)  
# this saves a report in html in working dir and later rendered in the notebook  
profile.to\_file("real\_data\_report\_ctgan.html")  
profile.to\_notebook\_iframe()
```
One of the most common ways to generate synthetic tabular data is via the CTGAN Model. The CTGAN model is based on the GAN-based deep learning data synthesizer, which was presented at the NeurIPS 2020 conference in the paper titled "Modeling Tabular Data Using Conditional GAN."

We can add constraints to the synthetic data generation process too. For example, some values might be valid only in a particular range. Also, some columns, like DOB and age, have a strict correlation that the model might get wrong. We can add these logics into the constraints and pass them as an argument when we create an instance of the model.


```
# we have already imported CTGAN from sdv.tabular  
# lets create an instance and fit it on the real data  
# lets time it too  
%%time  
model\_ctgan = CTGAN()  
model\_ctgan.fit(real\_data)
```

```
new\_data\_ctgan = model\_ctgan.sample(real\_data.shape[0])  
  
#lets generate a pandas profiling report on the new data too  
profile\_synthetic = ProfileReport(  
 new\_data\_ctgan,  
 title="Profiling Synthetic Adult Data",  
 html={"style": {"full\_width": True}},  
)  
profile\_synthetic.to\_file("fake\_data\_report\_ctgan.html")  
profile\_synthetic.to\_notebook\_iframe()
```
2. Image Synthetic Data

These images can be generated using computer graphics techniques or generative models such as Generative Adversarial Networks (GANs).

We can either talk about generating images from tags or from text. There are a lot of text-to-image data generators. In this article, we focus on the images generated, which can be used as synthetic data for training in specific cases.

Synthetic Image Generation with Variational Autoencoders (VAE)
--------------------------------------------------------------

Variational Autoencoders (VAEs) are a type of generative model that can be used to generate synthetic image data. VAEs are neural networks that learn to generate images by encoding an input image into a lower-dimensional representation, known as a latent representation or bottleneck, and then decoding the latent representation back into an image.

The encoding process is performed by an encoder network that maps an input image to its latent representation, while the decoding process is performed by a decoder network that maps the latent representation back to an image. The goal of VAEs is to learn a mapping from the input image space to the latent representation space that captures the underlying structure of the data.

One of the key features of VAEs is that they enforce a constraint on the distribution of the latent representations, which is typically modeled as a Gaussian distribution. This allows the VAE to generate new images by sampling from the Gaussian distribution and then decoding the samples back into images.

The generated images can be used as synthetic data for training and testing machine learning models, especially in domains where real-world data is scarce or privacy is a concern. VAEs have been shown to generate high-quality images that are similar to real-world data, making them a popular choice for image synthesis tasks.

In summary, VAEs are a type of generative model that can be used to generate synthetic image data by encoding and decoding images through a neural network architecture. They are a flexible and powerful tool for addressing data scarcity, data privacy, and data augmentation challenges in computer vision and machine learning.

Synthetic Image Generation with Generative Adversarial Networks (GAN)
---------------------------------------------------------------------

Generative Adversarial Networks (GANs) are a type of generative model that can be used to generate synthetic image data. GANs consist of two networks: a generator network and a discriminator network. The generator network learns to generate new images, while the discriminator network learns to distinguish between real images and generated images.

The two networks are trained together in an adversarial manner, with the generator trying to generate images that are indistinguishable from real images, and the discriminator trying to correctly classify real images from generated images. Over time, the generator and discriminator both improve, and the generator is able to generate increasingly realistic images.

GANs have been shown to be capable of generating high-quality synthetic images that are similar to real-world images. They have been used for many different things, such as image synthesis, image translation, and style transfer.

One of the key strengths of GANs is their ability to generate images that are diverse and representative of the data distribution. This makes them well-suited for data augmentation and data generation tasks in computer vision and machine learning.

In short, GANs are a type of generative model that can be used to make fake image data by training a generator network and a discriminator network to work against each other. In computer vision and machine learning, they are a powerful way to deal with problems like not having enough data, keeping data private, and adding to data.

Head over to <https://thispersondoesnotexist.com/> to look at some images generated by the legendary StyleGAN2/StyleGAN3.

Image Diffusion Models
----------------------

Image diffusion models are a type of generative model that can be used to generate synthetic image data. They are based on the idea of diffusion processes, which describe the spread of a substance or signal through a medium over time. Image diffusion models treat an image as a signal that diffuses over time, and generate synthetic images by simulating the diffusion process.

The key idea behind image diffusion models is to model the relationship between an image and its transformed versions. This relationship is modeled as a diffusion process, in which a series of diffusion steps change the image into a new image. Each diffusion step can be thought of as a step in the image generation process, and the final image is generated by aggregating the results of the diffusion steps.

There are several types of image diffusion models, including non-linear diffusion models, anisotropic diffusion models, and random walk models. These models can be used to make fake images that look like real ones. They have been used in a wide range of ways, such as to remove noise from images, fix damaged images, and make new images.

Image Synthesis with Deep Convolutional Generative Adversarial Networks (DCGANs): DCGANs are a type of GAN that use deep convolutional neural networks as both the generator and the discriminator. DCGANs are capable of generating high-quality synthetic images that are similar to real-world images.

Generative Flow Models: Generative flow models are a type of generative model that can be used to generate synthetic image data by transforming a simple noise input into a high-dimensional image. Generative flow models are based on the idea of normalizing flow, which transforms a simple noise input into a complex distribution.

Let’s implement synthetic image generation in a few different ways.

1. Generate fake faces with DCGANs
2. Synthetic Image generation with Flip. Generate new 2D images from a small batch of objects and backgrounds.
3. Text to Image Diffusion Model for photorealistic image generation

Generate fake faces with DCGANs
-------------------------------

I will be using four Nvidia A5000 RTX GPUs to generate these images since it is computationally very expensive.

Synthetic Image generation with Flip. Generate new 2D images from a small batch of objects and backgrounds
----------------------------------------------------------------------------------------------------------

We focus on image overlaying and making it look realistic. We will be using Flip for this demo.


```
# create a conda environment with Python (>= 3.7)Opencv (>= 4.3.0) Numpy (>= 1.19.1)  
# install flip  
pip install flip-data
```
Let’s make two directories, one for the background images and one for the objects to compose.

Object

ObjectBackground

BackgroundCombination

Overlayed ImagesText to Image Diffusion Model for photorealistic image generation
-----------------------------------------------------------------


```
from diffusers import StableDiffusionPipeline  
import torch  
  
model\_id = "runwayml/stable-diffusion-v1-5"  
# do not use half precision on CPU  
# I will recommend using GPU for inference cause the CPU inference is slooow  
# for GPU feel free to change the float point precision to 16 from 32 in the next line of code  
pipe = StableDiffusionPipeline.from\_pretrained(model\_id, torch\_dtype=torch.float32)  
# pipe = pipe.to("cuda")  
  
prompt = "a photo of a panda running through a field"  
image = pipe(prompt).images[0]   
   
# image.save("panda.png")  
image.show()
```
Image generated by the diffusion model from the prompt “a photo of a panda running through a field”3. Synthetic Text Data for OCR

I worked on OCR with Prudential, Singapore. OCR in real life is a prime example on OCR almost will never work in the wild without failsafes.

Also, ID Card data is sensitive so you need to generate your own.

We will be using the trdg library for this.


```
pip install trdg
```
Generate Images


```
from trdg.generators import (  
 GeneratorFromDict,  
 GeneratorFromRandom,  
 GeneratorFromStrings,  
 GeneratorFromWikipedia,  
)  
impor time  
  
# The generators use the same arguments as the CLI, only as parameters  
generator = GeneratorFromStrings(  
 ['Test1', 'Test2', 'Test3'],  
 blur=2,  
 random\_blur=True  
)  
  
for img, lbl in generator:  
 # Do something with the pillow images here.  
 img.show()  
 time.sleep(2)
```
Final Remarks
=============

Synthetic data has become a crucial tool in the field of machine learning and data science. The idea of generating artificial data to solve real-world problems is not new, but recent advances in deep learning and generative models have dramatically increased its capabilities and applications.

One of the key benefits of synthetic data is its ability to address data scarcity and privacy issues. In many real-world situations, collecting large amounts of high-quality data can be difficult or even impossible. Synthetic data can be generated in vast quantities to fill in the gaps and provide additional training data for machine learning algorithms. Additionally, synthetic data can be used to protect sensitive information, such as personal data or confidential business information, by creating artificial datasets that contain similar patterns and structures, but not actual sensitive information.

Another advantage of synthetic data is its ability to improve the performance of machine learning algorithms. By generating artificial data that resembles real-world data, synthetic data can be used to train machine learning algorithms in ways that are not possible with real data alone. This can help to overcome the limitations of real data, such as class imbalance or overfitting, and lead to better model performance. Additionally, synthetic data can be used to augment real-world data, creating larger, more diverse datasets that can help to improve the accuracy and robustness of machine learning algorithms.

In recent years, the development of deep learning and generative models has also made it possible to generate high-quality synthetic image data. From Variational Autoencoders (VAEs) to Generative Adversarial Networks (GANs), and Image Diffusion Models to Deep Convolutional Generative Adversarial Networks (DCGANs), there are many techniques available for generating synthetic image data. These techniques can be used to create artificial datasets that closely resemble real-world images, and can be used for a variety of purposes, such as training computer vision algorithms, testing image processing algorithms, and even generating high-quality animations.

In addition to its technical benefits, synthetic data also has the potential to impact other areas of life and business. For example, synthetic data can be used to support innovation in fields such as autonomous vehicles, healthcare, and finance. By generating vast amounts of synthetic data that resembles real-world data, researchers and developers can create and test new algorithms and technologies in a safe and controlled environment, before deploying them in real-world scenarios.

Despite its many advantages, synthetic data is not a silver bullet, and there are still challenges and limitations that need to be addressed. For example, while synthetic data can be generated in vast quantities, it may not accurately capture the complexity and diversity of real-world data. Additionally, synthetic data may not fully capture the relationships and interdependencies between different variables, leading to models that are not fully representative of the real world.

In conclusion, synthetic data has become an increasingly important tool in the field of machine learning and data science. From addressing data scarcity and privacy issues to improving model performance and creating augmented datasets, the applications of synthetic data are many and varied. Whether we are using tabular data or image data, the generation of synthetic data is a powerful tool for solving real-world problems and advancing the field of machine learning. As machine learning and data science continue to evolve, it is likely that synthetic data will play an even more important role in shaping the future of artificial intelligence and data science.

References

1. <https://www.kaggle.com/code/mcarujo/synthetic-data-generation-sdv-tutotial>
2. <https://www.kaggle.com/code/sayakdasgupta/fake-faces-with-dcgans>
3. <https://github.com/LinkedAi/flip>
