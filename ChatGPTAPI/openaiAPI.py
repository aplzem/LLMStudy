import ast
import openai
import pandas as pd
from scipy import spatial
import tiktoken
# 设置你的 OpenAI API 密钥
openai.api_key = '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'
# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

# test OPENAI Embedding
def test_openai_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002",
    )
    print(response['data'][0]["embedding"])


# test OPENAI Search
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 10
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def doc2embedding(strs):
    text = strs.replace("    ", "").split("\n")
    # 去掉list中的''元素
    text = list(filter(None, text))
    # 对list 中的每个元素，创建embedding，并保存为dataframe，dataframe中的每行构成为：第一列为text，第二列为embedding

    df = pd.DataFrame(
        [(s, openai.Embedding.create(input=[s], model=EMBEDDING_MODEL)["data"][0]["embedding"]) for s in text],
        columns=["text", "embedding"]
    )
    # 将df 保存为csv 文件
    df.to_csv("../data/testspeech.csv", index=False)
    return df


def test_openai_api(df):
    conversation = []
    while True:
        # 获取用户输入
        user_input = input("User: ")
        question = query_message(user_input, df, GPT_MODEL, 500)
        # 设定退出条件
        if user_input == 'exit':
            print("Bye!")
            print(conversation)
            break
        # 发送对话请求
        user_chat = {'role': 'user', 'content': question}
        conversation.append(user_chat)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )
        # 提取助手的回复
        assistant_reply = response.choices[0].message.content
        # reply = bytes(assistant_reply, 'utf-8').decode('unicode_escape')
        print("Assistant:", assistant_reply)
        # 更新对话历史
        # conversation.append({'role': 'user', 'content': user_input})
        conversation.append({'role': 'assistant', 'content': assistant_reply})


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = '请仅使用以下内容来回答后续问题。如果在所给的内容中，找不到答案，写“我找不到答案”。'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\n内容部分:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            print(num_tokens(message + next_article + question, model=model))
            break
        else:
            message += next_article
    return message + question

# 打开并读取txt 文件
def read_txt_file(path):
    with open(path, 'r') as f:
        content = f.read()
    return content


if __name__ == '__main__':
    # openai_multi_conversation
    # test_openai_api()
    # openai_embedding
    # test_openai_embedding("Hello, how are you today?")
    # DONE ALREADY: text to embedding, and save as csv file
    # ret = read_txt_file('../data/testspeech.txt')
    # embeds = doc2embedding(ret)

    #test qa
    df = pd.read_csv("../data/testspeech.csv")
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    print("done")
    test_openai_api(df)

