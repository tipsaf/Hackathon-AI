# Hackathon Polytechnique IRIS

## Our product

Welcome to the IRIS plant shop. With more than 50 products in our collection, we are happy to provide you assistance with the best language models on the market. We will find the best plant according to your preferences. Ask anything to the assistant and happy purchase!

## Setup

Lien vidéo démonstration: https://drive.google.com/file/d/1ipQ963HQt_kcmzxq25Hj2DP02rgDMDUZ/view?usp=sharing

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   cd hackathon_iris_group
   ```

4. Create a new virtual environment

   ```bash
   # Linux
   python -m virtualenv venv
   . venv/bin/activate
   ```

   ```shell
   # Windows
   python -m virtualenv venv
   venv\Scripts\activate
   ```

5. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

6. Run the app

   ```bash
   MISTRAL_API_KEY='YOUR-API-KEY' uvicorn app:app --reload --host 127.0.0.1 --port 5001
   ```
You should now be able to access the app at [http://localhost:5001](http://localhost:5001)! 
