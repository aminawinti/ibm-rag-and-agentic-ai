from config import CAPTION_QUERY, QUESTIONS
from shared import ask, build_model, encode_images


def main():
    model = build_model()
    encoded_images = encode_images()

    # 1. captioning
    print(f"Query: {CAPTION_QUERY}\n")
    for number, image in enumerate(encoded_images, 1):
        if image is None:
            continue  # download failed, already warned
        print(f"Image {number}: {ask(model, image, CAPTION_QUERY)}\n")

    # 2. QA
    for number, question in QUESTIONS:
        image = encoded_images[number - 1]
        if image is None:
            continue  # download failed, already warned
        print(f"Image {number} | {question}")
        print(f"  -> {ask(model, image, question)}\n")

if __name__ == "__main__":
    main()
