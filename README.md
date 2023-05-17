## Prerequisites

* Create a Bot in `@BotFather`

* Turn the inline mode ON in the `Bot Settings` -> `Inline Mode` -> `Turn inline mode ON`

* \>= `Python 3.6`

* Have a `.env` file inside the parent working directory.

* The `.env` file should contain your `bot_token`
```python 
bot_token=your_bot_token
```

## How to Run

### Manual

* If you want, you can setup a python `virtualenv` and use that to run the 
Bot.

    i) Create virtual environment : `virtualenv venv`

    ii) Activate environment : `source venv/bin/activate`


* `pip install -r requirements.txt`

* `python3 -m LibGenBot`

### Container(Docker)

 * **Building Docker Image Yourself**

       docker build -t image_name:latest .
    Replace `image_name` with whatever image name you wanna give. e.g.:

       docker build -t libgenbot:latest .

* **Pulling Image from DockerHub**

    I have already uploaded a Docker Image of Library Genesis Bot to DockerHub. Pull the image and run the container.

      docker pull adenosinetp10/libgenbot:latest

* **Running the Container**

    create a `.env` file and add the `bot_token` to it as stated in **Prerequisites**

    Then run the container by doing

      docker run --env-file ./.env libgenbot


