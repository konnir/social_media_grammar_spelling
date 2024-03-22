from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote
from fastapi.staticfiles import StaticFiles
from typing import Dict
import uvicorn
from starlette.responses import JSONResponse
from demo_texts.demo_messages import DemoMessages
from tweet_predict.tweets_predictor import TweetsPredictor

app = FastAPI()
origins = [
    "http://localhost:8082",  # Adjust the port if your frontend is served on a different one
    "http://127.0.0.1:8082",  # You can include multiple origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def main():
    return FileResponse('templates/index.html')

tweets_classifier = TweetsPredictor('/home/user/IdeaProjects/x_grammar_spelling/model')
demo_messages = DemoMessages()

@app.post("/correct_tweet")
async def correct_tweet(request: Request) -> Dict[str, str]:
    """
     Simple correction for the incoming text.
    :param request: Request, must have the data in body (multiple messages with keys)
    :return: Dict[str, str], in practice JSON with the response as "1" ore "0" per each text key.
    """
    try:
        form_data = await request.form()
        decoded_data = {key: unquote(value) for key, value in form_data.items()}
        results = {key: tweets_classifier.predict(value) for key, value in decoded_data.items()}
        return results
    except Exception as e:
        print(f"Error in correct_tweet server: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during processing. Please try again later.") from e

@app.post("/demo_message")
async def demo_message() -> JSONResponse:
    """
    Method to call a test demo generator to get random message from a test CSV
    :return: JSONResponse, random tweet with text (tweet text), label ("0" or "1"), error (OpenAI comment)
    """
    try:
        text = demo_messages.get_demo_tweet()
        label = str(demo_messages.get_demo_label(text))
        error = demo_messages.get_demo_error(text)
        response_content = {
            "text": text,
            "label": label,
            "error": error
        }
        return JSONResponse(content=response_content)
    except Exception as e:
        print(f"Error in demo_message server: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during processing. Please try again later.") from e

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8082, log_level="warning")
