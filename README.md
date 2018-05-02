# Pokedex Classifier

## Training

### Use the provided training data::

```angular2html
unzip dataset.zip
```

### Download and Prepare Training Data

1. Download Training Data via Bing Image Search API

```
./build_dataset.sh <api key> original_151.txt pokemon_images
```

2. Resize Training Data to 96x96
```
./resize_data.sh pokemon_images
```

3. Move prepared images into dataset directory
```
mv pokemon_images_small dataset
```

### Train the Network

```
./train.py --dataset dataset --model pokedex.model --labelbin lb.pickle
```



