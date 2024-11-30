from . import run_model

if __name__ == '__main__':
    prompt = input('Ask the model for a recommendation:')
    response = run_model(prompt)
    print(response.content)