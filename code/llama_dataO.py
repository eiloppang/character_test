import pandas as pd
import random
import ollama
import sys


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
        # Ollama를 사용하여 응답 생성 (파라미터 추가)
        response = ollama.generate(
            model='llama3',
            prompt=prompt,
            options={
                'temperature': 0.7,  # 창의성 조절 (0.0 ~ 1.0)
                'top_p': 0.9,        # 토큰 선택 다양성 (0.0 ~ 1.0)
                'num_predict': 2048, # 최대 생성 토큰 수
                'repeat_penalty': 1.1,  # 반복 패널티
                'top_k': 40,         # 상위 k개 토큰 중에서 선택
                'seed': random.randint(1, 10000)  # 랜덤 시드
            }
        )

        return response['response']
    except Exception as e:
        print(f"Error generating villain: {str(e)}")
        sys.exit(1)


def main():
    # CSV 파일 경로 설정 (실제 파일 경로로 변경 필요)
    csv_path = "C:/Users/admin/PycharmProjects/character_test/alldata_clean.csv"  # 여기에 실제 CSV 파일 경로를 입력하세요

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
