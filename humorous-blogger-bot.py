import streamlit as st
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.giphy import GiphyTools

from pydantic import BaseModel, Field
from typing import List

class BlogSegmentedOutput(BaseModel):
    segments: List[str] = Field(..., description="Blog post broken into naturally flowing segments where GIFs can be inserted")

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # GiphyAPI Key input
    giphy_api_key = st.sidebar.text_input(
        "Giphy API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://developers.giphy.com/dashboard/)."
    )
    if giphy_api_key:
        st.session_state.giphy_api_key = giphy_api_key
        st.sidebar.success("✅ Giphy API key updated!")

    st.sidebar.markdown("---")

def render_humorous_blog_preferences():
    st.markdown("---")

    # Row 1: Blog Essentials in 3 Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📝 Blog Setup")
        topic = st.text_input("Blog Topic", placeholder="e.g., My Gym Fail, Working From Bed")
        gif_type = st.multiselect(
            "Preferred GIF Style",
            ["Meme reactions", "Movie/TV clips", "Animal antics", "Cartoon snippets", "Surprise me!"]
        )

    with col2:
        st.subheader("🎙️ Story Voice")
        narrator = st.text_input("Narrator", placeholder="e.g., You, your cat, an alien")
        gif_frequency = st.selectbox(
            "GIF Placement Frequency",
            ["Just a few (2–3 total)", "Every 2–3 paragraphs", "After every funny moment", "Let the bot decide"]
        )

    with col3:
        st.subheader("🎯 Audience & Length")
        audience = st.text_input("Target Audience", placeholder="e.g., Gen Z, foodies, parents")
        blog_length = st.selectbox(
            "Blog Length",
            ["Short (300–500 words)", "Medium (600–800 words)", "Long (1000+ words)"]
        )


    # Row 2: Content Guardrails & Final Touches in 3 Columns
    st.subheader("🎯 Content Preferences & Finishing Touches")
    col4, col5, col6, col7 = st.columns(4)
    with col4:
        sensitive_topics = st.text_input("Topics to Avoid (optional)", placeholder="e.g., politics, religion")
    with col5:
        title_style = st.selectbox(
            "Blog Title Style",
            ["Clickbaity", "Punny", "Straightforward with a twist"]
        )
    with col6:
        ending_style = st.selectbox(
            "How Should It End?",
            ["A witty life lesson", "A fake 'sponsored by' ad", "Made-up expert advice", "A quirky call-to-action", "Just end with a laugh"]
        )
    with col7:
        humor_styles = st.multiselect(
            "Select Humor Style(s)",
            ["Sarcastic", "Satirical", "Wholesome", "Dark", "Slapstick / Over-the-top",
            "Deadpan / Dry", "Self-deprecating", "Wordplay / Puns", "Random / Absurd"]
        )

    funny_incident = st.text_area(
        "Funny Moment or Scene (optional)",
        placeholder="e.g., I once joined a Zoom call with a spaghetti filter on..."
    )

    # Final dictionary to return
    return {
        "topic": topic,
        "narrator": narrator,
        "audience": audience,
        "blog_length": blog_length,
        "humor_styles": humor_styles,
        "funny_incident": funny_incident,
        "gif_type": gif_type,
        "gif_frequency": gif_frequency,
        "sensitive_topics": sensitive_topics,
        "title_style": title_style,
        "ending_style": ending_style
    }

def generate_humorous_blog_post(user_blog_preferences): 
    topic = user_blog_preferences["topic"]
    narrator =  user_blog_preferences["narrator"]
    audience =  user_blog_preferences["audience"]
    blog_length =  user_blog_preferences["blog_length"]
    humor_styles = ", ".join( user_blog_preferences["humor_styles"])
    funny_incident =  user_blog_preferences["funny_incident"] or "N/A"
    gif_type = user_blog_preferences["gif_type"] 
    gif_frequency = user_blog_preferences["gif_frequency"]
    sensitive_topics = user_blog_preferences["sensitive_topics"] or "None"
    title_style =  user_blog_preferences["title_style"]
    ending_style =  user_blog_preferences["ending_style"]
    
    humorous_writer_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Humorous Writer Agent",
        role="Writes chill, funny blog posts that sound like a friend venting about a weird or awkward moment that just happened.",
        description=dedent("""
            You’re not trying to be funny. You’re not trying to be clever. You’re just telling someone what happened — a little messily, a little sheepishly — because it was weird or embarrassing and you kinda need to talk about it.

            Your job is to write a markdown-formatted blog post that feels like a casual voice note: honest, unpolished, and a little rambly. Like something you'd tell a friend in the middle of a catch-up text or standing by the coffee machine.

            Humor should come from the moment, not the language. No dramatic setups. No quirky metaphors. Just talk it out like you lived it, not like you’re reciting it to an audience.

            If a moment’s awkward, let it stay awkward. If a line falls flat, that’s fine too — it’s more real that way.
        """),
        instructions=[
            "Start the post with ### <title>",
            "Write only in paragraph format — no headers, bullet points, or image tags.",
            "Use markdown double line breaks (`\\n\\n`) between paragraphs — like pauses in actual speech.",
            "Sound like you're texting a close friend after something weird happened — not like you’re writing for a blog.",
            "Keep it loose, unpolished, and slightly rambly. Interrupt yourself if it feels natural. Tangents are fine, as long as they loop back.",
            "Use short, direct sentences. Don’t explain too much. Don’t over-describe. If it sounds like writing, tone it down.",
            "Avoid punchlines, “ta-da” moments, or structured comedy beats. Let the awkward parts sit awkward. Let the story fizzle instead of wrapping up.",
            "Do not invent jokes or exaggerated scenarios. Embellishment is fine, but only if it sounds like a natural overreaction you’d admit to in real life.",
            "Avoid bloggy phrasing (e.g., ‘Ah yes, the joys of…’, or ‘Reader, I…’). If it feels like something you'd read in a lifestyle piece, don’t write it.",
            "Don’t chase quirk. Don’t write like a character. You're a real person who got mildly wrecked by something dumb.",
            "Slang is okay — but only if it sounds like something you'd say out loud. No meme-speak, no irony-for-irony’s-sake.",
            "You can use callbacks if they happen naturally. But don’t engineer them like punchlines. Let them sneak in like passing thoughts.",
            "Metaphors are fine if they’re lazy, muttered, or accidental. If it sounds clever, sand it down.",
            "Endings shouldn’t feel like endings. Let the story fizzle out: a quiet joke, a fake sponsor, a sigh, or just a cut-off thought. Never summarize.",
            "Stick to the word count range requested: Short (~400), Medium (~700), Long (~1000+). Don’t pad or drag once the moment’s over."
        ],
        markdown=True
    )    

    # Minimal and focused prompt
    humor_prompt = f"""
    Generate a humorous blog post using the following preferences:

    Topic: {topic}  
    Narrator: {narrator}  
    Audience: {audience}  
    Humor Style(s): {humor_styles}  
    Blog Length: {blog_length}  
    Funny Moment to Include: {funny_incident}  
    Title Style: {title_style}  
    Ending Style: {ending_style}  
    Sensitive Topics to Avoid: {sensitive_topics}

    Write a well-structured, markdown-formatted blog post with a compelling and funny title.
    The tone should match the humor style(s) above and appeal to the intended audience.
    """
    humorous_blog_draft = humorous_writer_agent.run(humor_prompt).content
    blog_title = humorous_blog_draft.strip().splitlines()[0]

    content_splitter_agent = Agent(
        name="Content Splitter Agent",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description="Splits a blog post into segments based on a selected GIF placement preference, returning a structured list of text chunks suitable for inserting GIFs.",
        role="You’re a content segmentation assistant. Your job is to split the blog post into well-formed segments where a GIF could be placed, based on the user’s preference.",
        instructions=[
            "You will receive two inputs: the full blog text, and a string describing the preferred GIF placement frequency.",
            "The gif_frequency input will be one of the following options:",
            "- 'Just a few (2–3 total)' → Divide the blog into 2–3 fairly long chunks.",
            "- 'Every 2–3 paragraphs' → Divide into smaller segments, ideally after every 2 or 3 paragraphs.",
            "- 'After every funny moment' → Break the text where a joke or punchy moment lands (don’t force it — look for natural comedic beats).",
            "- 'Let the bot decide' → Use your judgment to split the blog into sections where GIFs would enhance rhythm, pacing, or comic relief.",
            "Don’t alter the blog content. Only split it.",
            "Try to end each segment at a natural pause: end of a thought, punchline, or transition.",
            "Do not insert any text, GIFs, or markers — just return a list of string segments.",
            "Return your result as a JSON object with a single key: 'segments'. Each segment should be a standalone string.",
        ],
        response_model=BlogSegmentedOutput,
        use_json_mode=True
    )

    split_prompt = f"""
    GIF Placement Preference: {gif_frequency}

    Blog Content:
    {humorous_blog_draft}

    Split this blog into natural sections where a GIF could be inserted, based on the specified frequency.
    """
    split_response = content_splitter_agent.run(split_prompt).content
    n = len(split_response.segments)

    gif_quote_generator_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="GIF Quote Generator Agent",
        role="Generates expressive, funny quotes to pair with blog segments for GIF search.",
        description=dedent("""
            You help match blog post segments to the perfect GIFs by crafting short, emotionally resonant quotes.

            You will receive:
            - A blog segment
            - A humor style (e.g. dry British, anime slapstick, bloggy wit)
            - A GIF type (e.g. facial reaction, pop culture, awkward fail, silent scream)

            Your job is to write a single quote — casual, expressive, and under 8 words — that reflects the vibe of the segment, matches the humor style, and fits the kind of GIF described.

            Think of it like writing the perfect Giphy search term or reaction caption.
        """),
        instructions=[
            "Your output must be a single quote, under 8 words.",
            "Match the humor style provided — adjust tone and phrasing accordingly.",
            "Reflect the GIF type — your quote should evoke the kind of reaction or image implied.",
            "Write like someone reacting *in the moment* — quick, casual, unpolished.",
            "Avoid hashtags, emojis, internet irony, or anything that feels like a post.",
            "Don’t describe what happened. Capture the *feeling* of what just happened.",
            "Never repeat the blog wording — echo the emotion, not the sentence.",
            "Avoid polished punchlines — muttered frustration, sarcasm, or confused panic is ideal."
        ],
        markdown=False
    )

    gif_selector_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="GIF Selector Agent",
        tools=[GiphyTools(api_key=st.session_state.giphy_api_key)],
        description=dedent("""
            You are a GIF selector for humor blog posts. Given a short expressive quote that captures the vibe of a blog segment,
            your task is to:

            - Use the quote to search Giphy for an appropriate reaction GIF.
            - Select one GIF that best matches the tone and emotion implied by the quote.
            - Return only the **direct URL** of the selected GIF.

            This is for a humorous blog, so GIFs should be expressive, fun, and vibe-aligned — but not overly meme-y or offensive.
        """),
        instructions=[
            "Use the provided quote as your Giphy search query.",
            "Choose the most fitting and expressive result from the Giphy tool.",
            "Return only the **direct URL** of the selected GIF — no markdown, no captions, no extra formatting.",
            "Avoid offensive, overly meme-driven, or inappropriate GIFs.",
        ],
        show_tool_calls=True
    )

    enriched_segments = [blog_title]
    for idx in range(n): 
        segment = split_response.segments[idx] 

        gif_quote_prompt = f"""
        Blog Segment:

        {segment}

        Humor Styles: {humor_styles}
        GIF Types: {gif_type}

        Write a short, expressive quote (max 8 words) that captures the emotional tone or vibe of this segment, matching the humor style and intended GIF type. Think of it as what someone would type into Giphy or blurt out mid-reaction. Return only the quote. No formatting, no markdown, no JSON.
        """
        quote = gif_quote_generator_agent.run(gif_quote_prompt).content.strip() 

        gif_selector_prompt = f"""
        Quote for Giphy Search:
        {quote}

        Use the quote to search for a relevant, funny, and expressive GIF. Return only the **GIF URL**.
        """

        gif_url = gif_selector_agent.run(gif_selector_prompt).content.strip()
        segment_with_gif = f"{segment}\n\n![gif]({gif_url})"
        enriched_segments += [segment_with_gif]

    enriched_blog_post = "\n\n".join(enriched_segments)

    return enriched_blog_post.strip()

def main() -> None:
    # Page config
    st.set_page_config(page_title="Humorous Blogger Bot", page_icon="📝", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📝 Humorous Blogger Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Humorous Blogger Bot — a Streamlit tool that turns your awkward moments and everyday misadventures into laid-back, laugh-out-loud blog posts, complete with relatable quotes and perfectly timed GIFs.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_blog_preferences = render_humorous_blog_preferences()

    st.markdown("---") 

    if st.button("🤣 Generate My Humorous Blog Post"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "giphy_api_key"):
            st.error("Please provide your Giphy API key in the sidebar.")
        else:
            with st.spinner("Writing something awkwardly hilarious just for you..."):
                blog_output = generate_humorous_blog_post(user_blog_preferences)
                st.session_state.humorous_blog = blog_output

    if "humorous_blog" in st.session_state:
        st.markdown(st.session_state.humorous_blog, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Blog Post",
            data=st.session_state.humorous_blog,
            file_name="humorous_blog_post.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main() 