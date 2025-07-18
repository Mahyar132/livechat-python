# Python Live Chat App

A lightweight and minimal live chat application built using only Python’s built-in `http.server` module.  
No frameworks or external libraries required — just pure Python.

## Features

- No dependencies (runs with standard Python)  
- Responsive layout for desktop and mobile  
- Real-time messaging with simple username login  
- Accessible via both `localhost` and local network (IP address + port)  
- Messages persist in a local file  
- Easy to run: just double-click the Python script to start the server  
- Runs on port 8080 by default

## How to Run

1. Download or clone the repository.  
2. Double-click `app.py` (or run with `python app.py`) to start the server.  
3. Open your browser and visit:  
   - Local: [http://localhost:8080](http://localhost:8080)  
   - Network (other devices on LAN):  
     Replace `localhost` with your local IP address, e.g. `http://192.168.1.10:8080`

## Project Structure

livechat-python/
├── app.py # Main Python server (double-click to run)
├── data.json # Stores messages persistently
├── LICENSE # License file
├── README.md # This file


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Made with ❤️ by mahyar132
Feel free to fork, improve, or give feedback!
