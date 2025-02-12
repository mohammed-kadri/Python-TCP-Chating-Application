# Chat Application

This is a chat application implemented in Python using the `socket`, `threading`, `tkinter` (for the client), `pickle`, and `PIL` (for the client) libraries. It allows multiple clients to connect to a server and exchange messages, both in a public chat room and in private conversations.

## Features

*   **Graphical User Interface (GUI - Client):** Uses `tkinter` and `customtkinter` for a user-friendly interface on the client side.
*   **Multi-Client Support (Server):** Handles multiple clients connecting and communicating simultaneously.
*   **Public and Private Chat:** Supports both a public chat room where all users can see messages and private conversations between individual users.
*   **Real-time Communication:** Messages are sent and received in real-time using sockets and threading.
*   **Nickname Registration:** Users are prompted to enter a nickname upon connection.
*   **User List:** Displays a list of currently connected users.
*   **Message Formatting:** Messages include the sender's nickname.
*   **Scrollable Chat Area (Client):** The chat area scrolls automatically to show the latest messages.
*   **Message Routing (Server):** The server correctly routes messages to either the public chat or the intended recipient in a private conversation.

## How to Run

1.  **Prerequisites:** Make sure you have Python 3 installed. You'll also need to install the required libraries:

    ```bash
    pip install tkinter pillow customtkinter
    ```

2.  **Run the server:** Execute the `server.py` script:

    ```bash
    python server.py
    ```

    Keep the server running in a terminal.

3.  **Run the client:** In a *separate* terminal, execute the `client.py` script:

    ```bash
    python client.py
    ```

4.  **Enter Nickname (Client):** When prompted, enter your desired nickname.

5.  **Start Chatting:** You can now start chatting in the public chat room. To start a private conversation, click the "Message" button next to a user's name in the user list.

## Code Overview

### `client.py`

This file contains the client-side logic of the chat application.

*   **`Client` Class:** Manages the GUI, handles sending and receiving messages, updates the user list, and implements the logic for switching between public and private chats.
*   **`gui_loop()`:** Creates and manages the main window and its elements.
*   **`receive()`:** Continuously listens for incoming messages from the server.
*   **`write()`:** Sends the message entered by the user to the server.
*   **`update_users_list()`:** Updates the displayed list of connected users.
*   **`switch_conversation()`:** Handles switching the chat display between the public chat and private conversations.

### `server.py`

This file contains the server-side logic of the chat application.

*   **Global Variables:** `clients` (list of client sockets) and `nicknames` (list of client nicknames).
*   **`send(message)`:** Sends a message to the appropriate recipient(s).
*   **`handle(client)`:** Handles communication with a single client.
*   **`broadcast_nicknames()`:** Sends the updated list of connected nicknames to all clients.
*   **`receive()`:** Accepts incoming client connections and starts a new thread to handle each client.

