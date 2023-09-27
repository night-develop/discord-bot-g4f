## Getting Started
1. Clone the GitHub repository:

```
git clone https://github.com/dovgan-developer/discord-bot-g4f.git
```

2. Navigate to the project directory:

```
cd discord-bot-g4f
```

3. (Recommended) Create a virtual environment to manage Python packages for your project:

```
python3 -m venv venv
```

4. Activate the virtual environment:
  ```
  source venv/bin/activate
  ```
5. Install the required Python packages from `requirements.txt`:

```
pip install -r requirements.txt
```

6. Create config file

```
cp example.config.json config.json
```

7. Set discord bot token

```json
...
"discord": {
  "token": "<discord-token>",
  "prefix": "/"
}
...
```

8. Run

```
python3 main.py
```

9. Build docker container
```
sudo docker build -t discord-bot-g4f .
```

10. Run docker container
```
sudo docker run -d --name discord-bot-g4f discord-bot-g4f
```

### [Discord bot based on g4f](https://github.com/xtekky/gpt4free)