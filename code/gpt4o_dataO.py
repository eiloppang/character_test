import pandas as pd
import random
import openai
import sys
import os

# 환경 변수에서 API 키 로드
openai.api_key = "YOUR_OPEN_KEY"


def load_and_select_traits(csv_path):
    try:
        # CSV 파일 로드
        df = pd.read_csv(csv_path)

        # 각 카테고리에서 랜덤하게 하나씩 선택
        appearance = random.choice(df['Appearance'].dropna().tolist())
        personality = random.choice(df['Personality'].dropna().tolist())
        ability = random.choice(df['Ability'].dropna().tolist())
        occupation = random.choice(df['Occupation'].dropna().tolist())

        return {
            'appearance': appearance,
            'personality': personality,
            'ability': ability,
            'occupation': occupation
        }
    except Exception as e:
        print(f"Error loading CSV file: {str(e)}")
        sys.exit(1)


def generate_villain(traits):
    # 프롬프트 생성
    prompt = f"""Create a villain character, inspired by these elements, making them central to who they are:
    Appearance: {traits['appearance']}
    Personality: {traits['personality']}
    Ability: {traits['ability']}
    Occupation: {traits['occupation']}
    """

    try:
        # OpenAI API를 사용하여 응답 생성
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=2048,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating villain: {str(e)}")
        sys.exit(1)


def main():
    # CSV 파일 경로 설정
    csv_path = "C:/Users/admin/PycharmProjects/character_test/alldata_clean.csv"

    print("Loading traits from CSV...")
    traits = load_and_select_traits(csv_path)

    print("\nSelected traits:")
    for category, trait in traits.items():
        print(f"{category.capitalize()}: {trait}")

    print("\nGenerating villain character...")
    print("=" * 50)

    villain_description = generate_villain(traits)

    print("\nGenerated Villain:")
    print("=" * 50)
    print(villain_description)
    print("=" * 50)


if __name__ == "__main__":
    main()
