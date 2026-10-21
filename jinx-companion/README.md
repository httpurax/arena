# Jinx Companion

A Windows desktop chat app for Minecraft: All the Mods 10 players. Jinx Companion runs on your PC outside any game, reads your Minecraft save files, and provides an AI assistant (Jinx) who knows your actual progress and can help you with quests and gameplay.

## What It Is

Jinx Companion is a standalone local web application that:

- Runs a web server on your Windows PC (port 8720)
- Opens a chat interface in your default browser
- Reads your FTB Quests progress from Minecraft ATM10 save files
- Provides an AI assistant persona (Jinx) who knows your current game state
- Helps you with quest progression, tips, and general Minecraft advice

## Quick Start

### Running the App

1. **Double-click `start.bat`** - This is the easiest way to start the app
   - It starts the Python server
   - The server opens exactly one browser tab to http://127.0.0.1:8720
     (`start.bat` itself does not open a browser, so you never get two tabs)
   - The server runs on port 8720 on localhost only

2. **Manual start** (if preferred):
   ```bash
   cd jinx-companion
   python server.py
   ```
   Then open http://127.0.0.1:8720 in your browser.

## Configuration

### Settings Panel

Click the **Settings** button in the chat interface to configure:

- **LLM Base URL**: The primary OpenAI-compatible API endpoint (default: `http://127.0.0.1:31415/v1`)
- **API Key**: Your API key for the LLM service
- **Model**: The model to use (default: `auto`)
- **Fallback Base URL**: Secondary endpoint to try if primary fails (default: `http://127.0.0.1:8080/v1`)
- **Minecraft Instance Path**: Path to your ATM10 instance (e.g., `C:\Users\YourName\Desktop\ATM10`)
- **World Name**: The name of your world save

Settings are automatically saved to `config.json` in the app directory when you click **Save Settings**.

### Config File Location

The configuration file `config.json` is stored in the same directory as the application (`jinx-companion/config.json`). You can also edit it manually with a text editor.

Example `config.json`:
```json
{
  "llm_base_url": "http://127.0.0.1:31415/v1",
  "api_key": "your-api-key-here",
  "model": "auto",
  "fallback_base_url": "http://127.0.0.1:8080/v1",
  "minecraft_instance_path": "C:\\Users\\YourName\\Desktop\\ATM10",
  "world_name": "New World"
}
```

## Files It Reads

Jinx Companion reads the following files from your Minecraft instance:

### Save Files (Read-Only)
- `<instance>/saves/<world>/ftbquests/*.snbt` - Your FTB Quests progress files
  - Contains completed quest IDs
  - Multiple files may exist; all are read

### Configuration Files (Read-Only)
- `<instance>/config/ftbquests/quests/chapters/*.snbt` - Chapter definitions
  - Contains chapter names, quests, their tasks and rewards
- `<instance>/config/ftbquests/quests/lang/en_us.snbt` - Quest display names
  - Contains human-readable names for quests, chapters and tasks
  - Both the single `lang/en_us.snbt` file and the split
    `lang/en_us/{chapter.snbt,chapters/*.snbt}` layout are supported

### Player Data (Read-Only)
- `<instance>/saves/<world>/playerdata/*.dat` - Player save
  - Gives the experience level and the current dimension
  - Gzipped NBT, decoded with Python's standard library only
- `<instance>/saves/<world>/level.dat` - Used as a fallback when no
  `playerdata` file is readable

If the player data cannot be read, these details are skipped silently and the
rest of the game state is still shown.

**Note**: The app only reads these files. It never modifies your Minecraft saves or configuration.

## Game State Information

Jinx uses the following information from your save files:

- **World Name**: Your current world
- **Player**: Your experience level and current dimension (when readable)
- **Chapters Progress**: How many chapters you've completed
- **Quests Progress**: Total quests completed vs total available
- **Completed Quests**: Names of up to 10 completed quests
- **Next Quests**: Names of up to 10 quests you haven't completed yet,
  in quest-book order
- **Up next (details)**: Up to 5 incomplete quests with their task
  requirements and reward names, e.g.

  ```
  Up next (details):
  1. Stockpile Stone (Getting Started)
     Tasks: Obtain 64x minecraft:stone
     Rewards: 100 XP
  2. Into the Nether (Getting Started) [locked]
     Tasks: Visit The Nether
  ```

  Quests whose dependencies are already completed come first, followed by
  still-locked quests (marked `[locked]`) and optional quests (marked
  `[optional]`). Hidden quests are never listed.

A chapter is considered "completed" when all of its quests are completed.

## Requirements

- Windows PC
- Python 3 (standard library only - no pip dependencies needed)
- A web browser
- An OpenAI-compatible LLM endpoint (local or remote)
- Minecraft ATM10 with FTB Quests mod

## Technical Details

### Server
- Listens on: `127.0.0.1:8720`
- Uses: Python's built-in `http.server` module
- No external dependencies required

### API Endpoints
- `GET /` - Main chat page
- `POST /chat` - Send a message, get a response
- `POST /settings` - Save configuration

### Chat Request Format
```json
{
  "message": "Your message here",
  "history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

### Chat Response Format
```json
{
  "reply": "Jinx's response here"
}
```

### Settings Request Format
```json
{
  "llm_base_url": "http://127.0.0.1:31415/v1",
  "api_key": "your-key",
  "model": "auto",
  "fallback_base_url": "http://127.0.0.1:8080/v1",
  "minecraft_instance_path": "C:\\path\\to\\instance",
  "world_name": "World Name"
}
```

## Running Tests

The app includes unit tests for the game state reader:

```bash
cd jinx-companion
python -m pytest tests/ -v
```

Tests verify:
- SNBT file parsing (including comma-less FTB Quests files and URLs in strings)
- Completed quests extraction
- Chapter definitions and quest details (tasks and rewards) loading
- Quest name loading
- Game state building, including the `Up next (details)` section
- Graceful behaviour when chapter, task, reward or language fields are missing
- Best effort player basics (experience level and dimension)
- Shipped `config.json` defaults and that exactly one browser tab opens

Tests are offline: they use local fixtures and temporary directories only.

## Troubleshooting

### Browser doesn't open
- Manually open http://127.0.0.1:8720
- Check that the server started (look for "Serving on http://127.0.0.1:8720" message)

### Connection errors
- Ensure your LLM endpoint is running
- Verify the base URL in Settings is correct
- Check that your API key is valid

### "Save not readable" message
- Verify the Minecraft instance path is correct
- Ensure the world name matches your save
- Check that FTB Quests files exist in the expected locations

### Port already in use
- Make sure nothing else is using port 8720
- You can change the port in `server.py` if needed

## License

This is a companion tool for personal use with Minecraft: All the Mods 10.

## Persona

Jinx is a sharp, friendly companion who knows Minecraft: All the Mods 10 deeply. She helps you progress through the pack and answers general questions. She has access to your actual game state from your save files, so she knows exactly what you've completed and what you should do next.
