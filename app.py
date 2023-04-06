from flask import Flask
from google.cloud import vision
import math
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
import json
from google.protobuf import json_format

app = Flask(__name__)

@app.route('/')
def detect_document_uri():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = "https://i.imgur.com/hVXJKTW.png"

    response = client.document_text_detection(image=image) 
    json_string = json_format.MessageToJson(response._pb)

    #json_string = open("dummy.txt").read().replace("'",  "\"")
    
    responseObj = json.loads(json_string)
    for page in response.full_text_annotation.pages:
        block_confidences = []
        for block in page.blocks:
            block_confidences.append(block.confidence)

            paragraph_confidences = []
            for paragraph in block.paragraphs:
                paragraph_confidences.append(paragraph.confidence)

                for word in paragraph.words: 
                    for symbol in word.symbols:
                        letterX = [] 
                        letterY = []
                        for coord in symbol.bounding_box.vertices:
                            letterX.append(coord.x) 
                            letterY.append(coord.y)                       
                        Lx1 = letterX[0]
                        Lx2 = letterX[1]
                        Ly1 = letterY[0]
                        Ly3 = letterY[2]
                        width = Lx2 - Lx1
                        height = Ly3 - Ly1                
                        print("<p>\n", symbol.text, ": \n width: ", width, "\n height: ", height, "</p>")
            
        print('<p>\nParagraph confidence: {}%</p>'.format((math.floor(sum(paragraph_confidences) * 1000)/10)/len(paragraph_confidences)))
        print('<p>Block confidence: {}%</p>'.format((math.floor(sum(block_confidences) * 1000)/10)/len(block_confidences)))

    for listCounter in range(1, len(response.text_annotations)):
        wordBounding = []
        wordData = response.text_annotations[listCounter]

        for boundingCoord in wordData.bounding_poly.vertices:
            wordBounding.append(boundingCoord.x)
        print("<p>\n {}: {}</p>".format(wordData.description, wordBounding))

    word_gap_list = []
    for i in range(0, len(response.text_annotations)-1):
        if (i > 0):
            W1x = responseObj['textAnnotations'][i]['boundingPoly']['vertices'][1]['x']
            W2x = responseObj['textAnnotations'][i + 1]['boundingPoly']['vertices'][0]['x']
            word_gap = W2x - W1x
            word_gap_list.append(word_gap)
    print("<p>\n word gap: \n{}</p>".format(word_gap_list))

detect_document_uri()
  
if __name__ == '__main__':
    app.debug = True
    app.run()