from flask import Flask, request
from google.cloud import vision
import math
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
import json
from google.protobuf import json_format
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET', "POST"])

def detect_document_uri():
    
    data = {}
    try:
        data = dict(request.get_json())
    except:
        pass
    finally:                
        with app.app_context():        

            client = vision.ImageAnnotatorClient()
            image = vision.Image()
            image.source.image_uri = "https://i.imgur.com/hVXJKTW.png"

            response = client.document_text_detection(image=image) 
            json_string = json_format.MessageToJson(response._pb)    
            responseObj = json.loads(json_string)
            
            for page in response.full_text_annotation.pages:
                block_confidences = []
                LsizeCont = []
                dataJson = {}
                for block in page.blocks:
                    block_confidences.append(block.confidence)
                    paragraph_confidences = []
                    for paragraph in block.paragraphs:
                        paragraph_confidences.append(paragraph.confidence)
                        for word in paragraph.words: 
                            Lsize = {}
                            LsizeCont.append(Lsize)
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
                                Lsize[symbol.text] = {"width": width, "height": height}
                                dataJson["Letter-Sizes"] = LsizeCont
                                # Lsize.append("{}: width: {}, height: {}".format(symbol.text, width, height))
                    
                Pconf = math.floor(sum(paragraph_confidences) * 1000)/10/len(paragraph_confidences)
                Bconf = math.floor(sum(block_confidences) * 1000)/10/len(block_confidences)
                dataJson["Paragraph-Confidence"] = Pconf
                dataJson["Block-Confidence"] = Bconf
            Wsize = {}
            for listCounter in range(1, len(response.text_annotations)):
                wordBounding = []
                
                wordData = response.text_annotations[listCounter]

                for boundingCoord in wordData.bounding_poly.vertices:
                    wordBounding.append(boundingCoord.x)
                Wsize[wordData.description] = wordBounding
                dataJson["Word-Bounding"] = Wsize

            word_gap_list = []
            Wgap = {}
            for i in range(0, len(response.text_annotations)-1):
                if (i > 0):
                    W1x = responseObj['textAnnotations'][i]['boundingPoly']['vertices'][1]['x']
                    W2x = responseObj['textAnnotations'][i + 1]['boundingPoly']['vertices'][0]['x']
                    word_gap = W2x - W1x
                    word_gap_list.append(word_gap)
            # Wgap["Gaps"] = word_gap_list
            dataJson["Gaps"] = word_gap_list

    # dataJson = {"Letter-Sizes": Lsize, "Pconf": Pconf, "Bconf": Bconf}
    # return [LsizeCont, Pconf, Bconf, Wsize, Wgap]
    return dataJson
  
if __name__ == '__main__':
    app.debug = True
    app.run()