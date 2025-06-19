# Humorous Blogger Bot

**Humorous Blogger Bot** is a witty Streamlit application that turns your awkward moments, everyday blunders, or bizarre tales into hilariously laid-back blog posts — complete with mood-matching quotes and perfectly timed GIFs. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and Giphy's search API, this tool crafts blog entries that feel like texting a friend mid-chaos.

## Folder Structure

```
Humorous-Blogger-Bot/
├── humorous-blogger-bot.py
├── README.md
└── requirements.txt
```

* **humorous-blogger-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Blog Preferences Input**
  Customize your blog with preferences like topic, narrator, humor style, length, ending vibe, and GIF placement strategy.

* **Natural Language Blog Generation**
  The `Humorous Writer Agent` produces a markdown-formatted blog that mimics a casual, slightly embarrassed storytelling tone — loose, honest, and funny in an offbeat way.

* **GIF-Ready Content Segmentation**
  The `Content Splitter Agent` divides the blog into segments based on your selected GIF frequency.

* **Mood-Matched Quote Generation**
  The `GIF Quote Generator Agent` creates expressive, short quotes based on each segment’s vibe and your humor preferences.

* **GIF Search & Embedding**
  The `GIF Selector Agent` uses Giphy to fetch and insert emotionally relevant GIFs, enriching each segment with visual flair.

* **One-Click Blog Preview & Download**
  View the fully rendered blog post in-app and download it as a `.md` file.

* **Responsive Streamlit Interface**
  Clean and engaging interface with a fun touch — built for expressive storytelling and creative journaling.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A Giphy API key ([Get one here](https://developers.giphy.com/dashboard/))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Humorous-Blogger-Bot.git
   cd Humorous-Blogger-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run humorous-blogger-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and Giphy API keys in the sidebar.
   * Fill in your blog preferences (topic, narrator, humor style, etc.).
   * Click **🤣 Generate My Humorous Blog Post**.
   * View your AI-generated post with embedded GIFs and download it.

3. **Download Option**
   Use the **📥 Download Blog Post** button to save your blog as a `.md` file.



## Code Overview

* **`render_humorous_blog_preferences()`**: Captures topic, narrator, humor style, and GIF preferences via structured Streamlit input layout.
* **`generate_humorous_blog_post()`**:

  * Uses the `Humorous Writer Agent` to create a markdown blog post.
  * Uses the `Content Splitter Agent` to break content for GIF placement.
  * Pairs segments with quotes via the `GIF Quote Generator Agent`.
  * Searches and inserts GIFs using the `GIF Selector Agent`.
* **`render_sidebar()`**: Manages API key storage in session state.
* **`main()`**: Controls UI layout, button logic, blog preview, and download.

## Contributions

Contributions are welcome!
Fork the repo, suggest features, report bugs, or open a pull request.
Let’s make weird storytelling even weirder — and funnier.
