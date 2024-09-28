### At submission time, delete the other `README.md` file and rename this to that.



To run the code, please do the following:
```
conda create -n spacestation python=3.10
conda activate spacestation
pip install -r requirements.txt
```

I don't anticipate there being any hiccups here, except for open3D, which isn't strictly necessary for the code to run.

Now, download ModelNet40 and unzip it into this directory (`denoising_model_net/`) with:
```
wget http://modelnet.cs.princeton.edu/ModelNet40.zip
unzip ModelNet40.zip
rm ModelNet40.zip
```

Finally, try:
```
python -m data.utils
```

This will show an airplane from the dataset, and you will be able to visualize the two types of degradation I am applying to the data (Gaussian noise and missing points).
