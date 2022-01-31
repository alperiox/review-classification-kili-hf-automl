# Opinion Classification with Kili Technology and HuggingFace AutoML

The project repository for this article.

Just clone the repository and download the models by using `scripts/download_models.py`

I haven't included the torch installation in the `requirements.txt`. That's because the installation procedure wouldn't be same for everyone. 

I have used `PROJECT_ID` and `KILI_API_KEY` environment variables to pass the API key and the project ID. I was using `dotenv` to load the environment variables from `.env` file. 


### Scripts usage:

`collect_reviews.py`

Script to collect the reviews by using [google-play-scraper](https://pypi.org/project/google-play-scraper/)

>> Arguments

> lang (l): The language reviews written in, default: English
> 
> country (c): The country to pull the reviews from, default: US
> 
> name (n): Package name of the application (Google Play Store)
> 
> count (co): Number of reviews to collect, default:10, `all` to get all reviews
> 
> filter (f): Integer to filter the reviews by rating, None for all rating. default: None
> 
> help: Shows the argument descriptions

>> Usage

> python scripts/collect_reviews.py -co 100 --name medium.com.reader

`download_models.py`

Downloads the pre-trained models (finetuned models for 40 and 20 runs) into the current working directory. Uses [gdown](https://github.com/wkentaro/gdown) to download the models from google drive. Folder ID can be found in the script file

>> Arguments

> None

>> Usage

> python scripts/download_models.py

`move_diff_to_review.py`

Moves the distinct elements of the given two datasets into `To Review` section in the project.

>> Arguments

> first: first CSV dataset to load,
> 
> second: second CSV dataset to load

>> Usage

> python scripts/move_diff_to_review.py --first data/processed/dataset-2.csv --second data/processed/dataset-3.csv

`prepare_dataset.py`

Pulls the labeled and reviewed data separately and saves it with the given file name in `data/processed` folder. 


>> Arguments

> output_name: File name for the pulled dataset. (it should include .csv extension too)
> 
> remove (optional): Label to remove from the dataset 


>> Usage

> python scripts/prepare_dataset.py --output_name final_dataset.csv
