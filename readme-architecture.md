## **Architecture Document: Terminal Client**

---

### **Overview**
The **Terminal Client** application provides an interactive chat interface using **REST API** to communicate with an AI-powered backend. It allows users to query the system and receive real-time responses, including references to external sources. This document outlines the architecture, components, and workflow of the client.

---

## **Architecture Diagram**

```
+--------------------------+
|      User Interface      |
| (Terminal-based Chat App)|
+--------------------------+
             |
             |
             V
+--------------------------+   
|  Terminal Client Layer |
| - Sends Queries          |
| - Processes Responses    |
| - Logs Data              |
+--------------------------+
             |
             |
             V
+--------------------------+
|      REST API Layer      |
| Perplexica API Backend   |
| - Processes Queries      |
| - Returns Responses      |
| - Provides References    |
+--------------------------+
             |
             |
             V
+--------------------------+
|     External Sources     |
|   (Articles, Web Pages)  |
+--------------------------+
```

---

### **Components**

1. **User Interface Layer (chat.py)**
   - Terminal-based interface where the user interacts with the chatbot.
   - Displays **colored responses** and **query results** to the user.
   - Captures **user input** and triggers queries to the API.

2. **Perplexica Client Layer (perplexica_client.py)**
   - Encapsulates all logic to communicate with the **Perplexica REST API**.
   - Manages **chat history**, **source logging**, and **timeout handling**.
   - Handles **API errors** and ensures a smooth user experience.
   - Uses `requests` to send and receive data from the backend.

3. **REST API Layer**
   - The Perplexica backend processes incoming requests from the client.
   - Uses **chat models** and **embedding models** to generate responses.
   - May return references to **external sources** along with the responses.

---

### **Workflow**

1. **User Interaction**:
   - The user interacts with the app via the **terminal chat interface**.
   - They type a query, which is **captured** by the `chat.py` script.

2. **Request Handling**:
   - The **PerplexicaClient** sends the query to the API using the **REST endpoint** `/api/search`.
   - It waits for a response and handles **timeouts** gracefully.

3. **Response Processing**:
   - If **sources** are provided in the response, the client logs them and prints them to the user.
   - If there is an **error** or **timeout**, appropriate messages are displayed to the user.

4. **Logging**:
   - All **activities and sources** are logged to `activity.log`.
   - **Chat history** is stored in `chat_history.log` for reference.