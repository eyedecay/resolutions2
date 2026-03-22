import argparse
import requests
import sys

BASE_URL = "https://api.jikan.moe/v4/anime"


def get_anime_info(name):
    """
    Gets full anime synopsis
    Args:
        name (str)
    Returns:
        None
    """
    url = f"{BASE_URL}?q={name}&limit=1"
    req = requests.get(url)
    if req.status_code != 200:
        print("API error")
        sys.exit(1)
    data = req.json()
    print(f"{name.upper()}: {data['data'][0]['synopsis']}")

def get_top_anime(number):
    """
    Gets top number ranked anime
    Args:
        number (int)
    Returns: 
        None
    """
    url = f"https://api.jikan.moe/v4/top/anime?limit={number}"
    req = requests.get(url)

    if req.status_code != 200:
        print("API error")
        sys.exit(1)
    
    data = req.json()
    print("Top ANIME")
    for anime in data["data"]:
        print(f"Name: {anime['title']}, score: {anime['score']}, Rank: {anime['rank']}")

def compare_anime(anime1, anime2, score = False, episodes = False):
    """
    Compares score and # of episodes of 2 animes (or not if mutually exclusive used)
    Args:
        anime1 (str)
        anime2 (str)
        score (bool)
        episodes (bool)
    """
    url1 = f"{BASE_URL}?q={anime1}&limit=1"
    url2 = f"{BASE_URL}?q={anime2}&limit=1"
    req1 = requests.get(url1)
    req2 = requests.get(url2)
    if req1.status_code != 200 or req2.status_code != 200:
        print("API Error")
        sys.exit(1)
    
    data1 = req1.json()
    data2 = req2.json()

    anime1 = data1['data'][0]
    anime2 = data2['data'][0]
    output = f"Comparing {anime1['title'].upper()} vs {anime2['title'].upper()}\n"
    if score:
        output += f"Score: {anime1['score']} vs {anime2['score']}\n"
    elif episodes:
        output += f"Episodes: {anime1['episodes']} vs {anime2['episodes']}"
    else:
        output += (f"Score: {anime1['score']} vs {anime2['score']}\n"
                   f"Episodes: {anime1['episodes']} vs {anime2['episodes']}")
    print(output)

def main():
    """main"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = "command")

    info_parser = subparsers.add_parser("info", help = "Get anime info")
    info_parser.add_argument("name", type = str, help = "Full anime synopsis")

    top_parser = subparsers.add_parser("top", help = "Get Top anime")
    top_parser.add_argument("number", type = int, help = "How many do you want to see")

    compare_parser = subparsers.add_parser("compare", help = "Compare two animes")
    compare_parser.add_argument("anime1", type = str, help = "Select an anime")
    compare_parser.add_argument("anime2", type = str, help ="Select an anime")

    group = compare_parser.add_mutually_exclusive_group()
    group.add_argument("--score", action="store_true", help="Compare by rating only")
    group.add_argument("--episodes", action="store_true", help="Compare by episodes only")

    args = parser.parse_args()

    if args.command == "info":
        name = args.name
        get_anime_info(name)
    elif args.command == "top":
        get_top_anime(args.number)
    
    elif args.command == "compare":
        compare_anime(args.anime1, args.anime2, args.score, args.episodes)

if __name__ == "__main__":
    main()