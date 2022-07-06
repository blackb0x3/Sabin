import os, requests, shutil

TEST_ASSETS_DIR_NAME = 'TestAssets'
png_url = "https://img.pokemondb.net/artwork/vector/large/"
jpg_url = "https://img.pokemondb.net/artwork/large/"

github_pokemon_data_url = "https://raw.githubusercontent.com/fanzeyi/pokemon.json/master/pokedex.json"
pokedex = requests.get(github_pokemon_data_url).json()
pokemon_names = [pokemon["name"]["english"].lower().replace(" ", "-").replace(".", "") for pokemon in pokedex]

assets_folder_path = os.path.join(os.path.curdir, TEST_ASSETS_DIR_NAME)
if not os.path.exists(assets_folder_path):
    os.mkdir(assets_folder_path)

for name in pokemon_names:
    for extension, url in {'png': png_url, 'jpg': jpg_url}.items():
        if not os.path.exists(os.path.join(assets_folder_path, f'{name}.{extension}')):
            img_resp = requests.get(f"{url}{name}.{extension}", stream=True)

            if img_resp.ok:
                with open(f"{TEST_ASSETS_DIR_NAME}/{name}.{extension}", 'wb') as img:
                    shutil.copyfileobj(img_resp.raw, img)
                print(f"Downloaded ./{TEST_ASSETS_DIR_NAME}/{name}.{extension}")
        else:
            print(f'already found ./{TEST_ASSETS_DIR_NAME}/{name}.{extension}')
