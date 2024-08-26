# Lunar Terrain Segmentation Web Application

Hey, this repository will help you set up your webapp for lunar image segmentation.
* I have used FastAPI for building the API
* I have used Streamlit for the Frontend

## Setup
1. Clone or Download the Repository and open the project directory in your editor (VS Code)
2. Create your virtual environment using `python -m venv <name_of_the_venv>`
3. Activate your virtual environment using `.\<name_of_the_venv>\Scripts\activate`
4. Install the requirements using `python -m pip install -r requirements.txt`
5. You can train your model using the [`train_model.ipynb`](https://github.com/SpartificialUdemy/lunar-segmentation-app/blob/main/train_model.ipynb) python notebook via [Kaggle](https://www.kaggle.com/)
6. Add your trained model in [`models`](https://github.com/SpartificialUdemy/lunar-segmentation-app/tree/main/models) and remove if there are other models present there
7. In command prompt first run your FastAPI app:- `uvicorn backend:app --reload`
8. Then again open command prompt and run the streamlit app:- `streamlit run frontend.py`

## About Trained Model used in this app
* This model is trained using UNET with VGG16 Backbone
* The data used for the training can be found on [Kaggle](https://www.kaggle.com/datasets/romainpessia/artificial-lunar-rocky-landscape-dataset)
* We used first 8000 images from `render` (artificially generted Moon terrain) & `clean` (respective masks) directories for training.
* We used all the other remaining images for validation except the last 4 which we used as test set.
* This model on Validation set gave 80% IOU on average.
* The model was trained as a part of training program at [Spartificial](https://spartificial.com/).
