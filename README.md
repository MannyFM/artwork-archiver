# artwork-archiver
Small python script to download artworks from Spotify.

Script consists of 2 parts `main.py` and `dump_artworks.py`. First script fetches all tracks added to user library in Spotify and stores them list of albums of them in `dump.json` for further download. Second script reads that json and downloads all that artworks in `output` folder.

Firstly, you need python3 and pip to use this script.
In order to install other dependencies run.
```
pip install -r requirements.txt
```

To run first part you need to configure Spotify API in `config.json` file. After you do this you can pass Spotify username as argument or when program prompts you

```
python main.py [username]
```

If everything goes alright, you can fetch artworks just by running second Script
```
python dump_artworks.py
```
