from typing import List, Optional
from urllib.parse import quote

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# typically, you wont put API key in code, but its necessary for this challenge
API_KEY = "eb86a9144e200d6ce1dc401bdebed3cdf6511c5c"
BASE_URL = "http://www.giantbomb.com/api"

class Game(BaseModel):
    id: int
    name: str
    deck: Optional[str] = None
    thumb_url: str = "not found"
    aliases: str = "not found"

checked_out_games = set()

async def search_games(query: str) -> List[Game]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        encoded_query = quote(query)
        url = f"{BASE_URL}/search/?api_key={API_KEY}&format=json&query={encoded_query}&resources=game"
        
        headers = {
            "User-Agent": "MyGameRentalApp/1.0",
        }
        
        print(f"Requesting URL: {url}")  # Debug print
        
        response = await client.get(url, headers=headers)
        
        print(f"Response status: {response.status_code}")  # Debug print
        print(f"Response headers: {response.headers}")  # Debug print
        
        if response.status_code == 200:
            data = response.json()
            games = []
            for game_data in data.get("results", []):
                game = Game(
                    id=game_data["id"],
                    name=game_data["name"],
                    deck=game_data.get("deck"),
                    thumb_url=game_data.get("image", {}).get("thumb_url", "not found"),
                    aliases=game_data.get("aliases") or "not found"
                )
                games.append(game)
            if len(games) == 0:
                game = Game(
                    id=0,
                    name="not found",
                    deck="not found",
                    thumb_url="not found",
                    aliases="not found"
                )
                games.append(game)
                
            return games
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch games: {response.text}")

@app.get("/search/{query}", response_class=HTMLResponse)
async def search(query: str):
    games = await search_games(query)
    html_content = "<h1>Search Results</h1>"
    for game in games:
        html_content += f"""
        <div>
            <h2>{game.name}</h2>
            <img src="{game.thumb_url}" alt="{game.name}">
            <p>{game.deck or 'No description available'}</p>
            <p>Aliases: {game.aliases}</p>
            <a href="/checkout/{game.id}">Checkout</a>
        </div>
        <hr>
        """
    return HTMLResponse(content=html_content)

@app.get("/checkout/{game_id}", response_model=dict)
async def checkout_game(game_id: int):
    if game_id in checked_out_games:
        raise HTTPException(status_code=400, detail="Game already checked out")
    checked_out_games.add(game_id)
    return {"message": f"Game with ID {game_id} has been checked out"}

@app.get("/checked_out", response_model=List[int])
async def get_checked_out_games():
    return list(checked_out_games)