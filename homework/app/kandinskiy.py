import requests, time, os, json, base64
from dotenv import dotenv_values


class FusionBrainAPI:
    def __init__(self, url, key, secret):
        self.URL = url
        self.AUTH_HEADERS = {
            "X-Key": f"Key {key}",
            "X-Secret": f"Secret {secret}"
            }

    def is_available(self, pipeline_id):
        response = requests.get(self.URL + f"key/api/v1/pipeline/{pipeline_id}/availability", headers=self.AUTH_HEADERS)
        data = response.json()
        return data["status"]
          

    def get_pipeline(self):
        response = requests.get(self.URL + "key/api/v1/pipelines", headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]["id"]

    def send_prompt(self, *, height, width, style, query, negative_prompt=None, pipeline):
        
        params = {
            "type": "GENERATE", 
            "style": style,
            "width": int(width),
            "height": int(height),
            "numImages": 1,
            "generateParams": {
                "query": query
            }

        }
        
        if negative_prompt is not None:
            params["negativePromptDecoder"] = negative_prompt

        data = {
            "pipeline_id": (None, pipeline),
            "params": (None, json.dumps(params), "application/json")
        }       

        response = requests.post(self.URL + "key/api/v1/pipeline/run", 
headers=self.AUTH_HEADERS, files=data)

        data = response.json()
        print(data)
        return data['uuid']

    
    def get_image(self, request_id, attempts=10, delay=5):
        while attempts > 0:
            response = requests.get(self.URL + "key/api/v1/pipeline/status/" + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            
            if data["status"] == "DONE":
                return data["result"]["files"]

            attempts -= 1
            time.sleep(delay)



def setup():
    config = dotenv_values(".env")
    api = FusionBrainAPI("https://api-key.fusionbrain.ai/", config["KAND_API"], config["KAND_SECRET"])
    return api.get_pipeline()
            
def generate_image(prompt_params, pipeline_id):
    config = dotenv_values(".env")

    api = FusionBrainAPI("https://api-key.fusionbrain.ai/", config["KAND_API"], config["KAND_SECRET"])
    

    prompt_params["pipeline"] = pipeline_id
    
    request_id = api.send_prompt(**prompt_params)
    image = api.get_image(request_id)[0]

    with open(f"./static/{request_id}.png", "wb") as f:
        f.write(base64.b64decode(image))
        return f"{request_id}.png"

def is_available(pipeline_id):
    config = dotenv_values(".env")
    api = FusionBrainAPI("https://api-key.fusionbrain.ai/", config["KAND_API"], config["KAND_SECRET"])
    return api.is_available(pipeline_id)
    
def get_styles():
    response = requests.get("https://cdn.fusionbrain.ai/static/styles/key")
    return response.json()
    

if __name__ == "__main__":
    config = dotenv_values(".env")

    api = FusionBrainAPI("https://api-key.fusionbrain.ai/", config["KAND_API"], config["KAND_SECRET"])
    
    pipeline_id = api.get_pipeline()
    print("in main")
    prompt_params = {
        "height":256,
        "width":256,
        "style": "ANIME",
        "query": "большой камень",
        "pipeline": pipeline_id,
        "negative_prompt": None
    }

    request_id = api.send_prompt(**prompt_params)
    image = api.get_image(request_id)[0]

    with open(f"./static/{request_id}.png", "wb") as f:
        f.write(base64.b64decode(image))
        print(f"saved in {request_id}.png")
