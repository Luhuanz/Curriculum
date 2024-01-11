
from pk_qa import PokemonKGQA

if __name__ == "__main__":
    handler = PokemonKGQA()
    while True:
        question = input("用户：")
        if not question:
            break
        answer = handler.answer(question)
        print("回答：", answer)
        print("*"*50)