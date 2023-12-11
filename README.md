# Canada Citizenship Study Guide

This project is a study assistant for the Canada Citizenship Test. It uses the OpenAI API to create and manage a study assistant that can help users prepare for the test.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip
- An OpenAI API key

### Installing

1. Clone the repository to your local machine:

```bash
git clone https://github.com/moonheelee/canada-citizenship-study-guide.git
```

2. Navigate to the project directory:

```bash
cd canada-citizenship-study-guide
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:

```bash
echo "OPENAI_API=your_api_key" > .env
```

Replace `your_api_key` with your actual OpenAI API key.

### Usage

1. Run `create_assistants.py` to create the study assistant:

```bash
python create_assistants.py
```

2. Run `app.py` to start the application:

```bash
streamlit run app.py
```

The application is a Streamlit app, so it will start a web server and open your default web browser to display the app.

## Built With

- [Python](https://www.python.org/)
- [OpenAI](https://www.openai.com/)
- [Streamlit](https://streamlit.io/)

## Slide for Demo

- [Something Fun with Assistants API](https://docs.google.com/presentation/d/160Q8debqkARUrvIw6t91uaxFV1gdDgjw-c-sl3A91X8/edit?usp=sharing)

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.