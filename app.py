from flask import Flask
from google.cloud import vision
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

@app.route('/')
def detect_document_uri():
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"

        response = client.document_text_detection(image=image)

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                print('\nBlock confidence: {}\n'.format(block.confidence))

                for paragraph in block.paragraphs:
                    print('Paragraph confidence: {}'.format(
                        paragraph.confidence))

                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        print('Word text: {} (confidence: {})'.format(
                            word_text, word.confidence))

                        for symbol in word.symbols:
                            print('\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence))

        # if response.error.message:
        #     raise Exception(
        #         '{}\nFor more info on error messages, check: '
        #         'https://cloud.google.com/apis/design/errors'.format(
        #             response.error.message))

        return jsonify(response)


if __name__ == '__main__':
        app.debug = True
        app.run()