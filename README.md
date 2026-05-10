# 🧠 renshuu2anki

> Personal automation tool for converting Japanese sentences from Renshuu into Anki flashcards.

---

## 📄 License

This repository includes a `LICENSE` file.
Please refer to `LICENSE` for the current licensing terms and usage permissions.

---

## ✨ Features

- Fetch sentence lists from the Renshuu API
- Clean and normalize Japanese text
- Remove noise like unnecessary parentheses
- Convert sentences into Anki flashcards automatically
- Prevent duplicate cards using a unique Renshuu ID
- Lightweight and simple execution — no server required

---

## ⚙️ Requirements

| Requirement | Details |
|---|---|
| Python | 3.10+ |
| Anki Desktop | Must be running during sync |
| AnkiConnect | Add-on ID: `2055492159` |
| Renshuu API key | See setup below |

---

## 🚀 Installation

```bash
git clone https://github.com/your-username/renshuu2anki.git
cd renshuu2anki
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
RENSHUU_API_KEY=your_api_key_here
```

---

## ⚠️ Required Anki Setup

Before running the sync, you must add a custom field to your Anki note type.

### Add the `RenshuuID` field

1. Open **Anki**
2. Go to **Tools → Manage Note Types**
3. Select your note type (e.g. `Basic`)
4. Click **Fields → Add**
5. Name it `RenshuuID`
6. Save changes

### Why this field is required

The `RenshuuID` field is used to:

- Prevent duplicate cards
- Enable safe re-syncing
- Identify each sentence uniquely

Without it, duplicate cards will be created and syncs will not be idempotent.

### Recommended field mapping

| Field | Content |
|---|---|
| `Front` | Japanese sentence |
| `Back` | English translation |
| `RenshuuID` | Unique sentence ID |

### Deck name

By default, cards are added to a deck named `🇯🇵`. You can change this by setting the `ANKI_DECK_NAME` environment variable in your `.env` file:

```env
ANKI_DECK_NAME=My Japanese Deck
```

Or edit it directly in `app/anki/client.py`:

```python
self.deck_name = os.getenv("ANKI_DECK_NAME", "🇯🇵")
```

---

## 📋 Renshuu Setup

Before syncing, you need a sentence list created on Renshuu and its list ID.

### 1. Create a sentence list

Go to the link below to create a new sentence list:

```
https://www.renshuu.org/index.php?page=custom/list_edit&booktype=sent&action=new
```

Add sentences, give your list a name, and save it.

### 2. Find your list ID

Open your list — the URL will look like this:

```
https://www.renshuu.org/lesson/c/10626774/sent/
```

The number between `/c/` and `/sent/` is your list ID. In this example: `10626774`.

### 3. Configure the list ID

Open `main.py` and replace the value of `RENSHUU_LIST_ID`:

```python
# Renshuu list ID used as the source of sentences to sync
RENSHUU_LIST_ID = 10626774  # ← replace with your list ID
```

---

## ▶️ Usage

Make sure **Anki is open** and **AnkiConnect is running**, then:

```bash
python main.py
```

By default, it syncs the configured list ID `10626774`.

---

## 🧠 How It Works

```
Renshuu API
   ↓
Parser (normalize Japanese text)
   ↓
Sync Service
   ↓
AnkiClient (via AnkiConnect)
   ↓
Anki Deck
```

---

## 🗂️ Project Structure

```
app/
 ├── anki/         # AnkiConnect client
 ├── renshuu/      # API client + parser
 ├── models/       # Sentence model
 ├── services/     # Sync orchestration
 └── settings.py   # Environment config
main.py            # Entry point
```

---

## 🧪 Example Output

```
Added: 外は寒いのに、電車の中は暑すぎた。
Added: 先生、テストのことで質問があるんですが。
Added: 別に忙しくないので、遊ぼう。
```

---

## 🔒 Duplicate Protection

Each note includes a `RenshuuID` field, which ensures:

- No duplicate cards are ever created
- Syncing can be run repeatedly without side effects
- Cards can be updated consistently over time

---

## 🧑‍💻 Author

Built by **Yumiko** ✨  
A personal automation tool for Japanese learning.