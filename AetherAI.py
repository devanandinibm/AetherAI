!pip install -q gradio pandas plotly
import gradio as gr
import pandas as pd
import plotly.express as px
import uuid


models = [
    {
        "id": "aethergpt-pro",
        "name": "AetherAI Pro",
        "developer": "Aether Labs",
        "category": "Large Language Models",
        "description": "Enterprise-grade language model for reasoning, content generation and intelligent automation.",
        "price": 2499,
        "benchmark": 94,
        "trust": 96,
        "accuracy": 93,
        "latency": 420,
        "deployments": 12450,
        "reviews": 843,
        "rating": 4.8,
        "verified": True
    },
    {
        "id": "visionforge-cv",
        "name": "VisionForge CV",
        "developer": "VisionForge",
        "category": "Computer Vision",
        "description": "High-performance computer vision model for detection, classification and visual analysis.",
        "price": 1899,
        "benchmark": 91,
        "trust": 93,
        "accuracy": 96,
        "latency": 180,
        "deployments": 9870,
        "reviews": 624,
        "rating": 4.7,
        "verified": True
    },
    {
        "id": "medinsight-ai",
        "name": "MedInsight AI",
        "developer": "MedIntel Research",
        "category": "Healthcare AI",
        "description": "AI assistance for medical information analysis, research and clinical documentation support.",
        "price": 3999,
        "benchmark": 95,
        "trust": 98,
        "accuracy": 97,
        "latency": 510,
        "deployments": 4320,
        "reviews": 391,
        "rating": 4.9,
        "verified": True
    },
    {
        "id": "bharatspeech",
        "name": "BharatSpeech",
        "developer": "Indic AI Labs",
        "category": "Speech and Audio",
        "description": "Multilingual speech recognition and synthesis optimized for Indian languages.",
        "price": 1499,
        "benchmark": 89,
        "trust": 92,
        "accuracy": 91,
        "latency": 220,
        "deployments": 15600,
        "reviews": 1120,
        "rating": 4.6,
        "verified": True
    },
    {
        "id": "pixelcraft",
        "name": "PixelCraft",
        "developer": "Pixel Labs",
        "category": "Image Generation",
        "description": "AI image generation for creative workflows, design and marketing.",
        "price": 1299,
        "benchmark": 88,
        "trust": 90,
        "accuracy": 89,
        "latency": 350,
        "deployments": 21340,
        "reviews": 1750,
        "rating": 4.5,
        "verified": True
    },
    {
        "id": "finsight-ai",
        "name": "FinSight AI",
        "developer": "QuantEdge",
        "category": "Finance AI",
        "description": "AI-powered financial analysis for forecasting, reporting and business insights.",
        "price": 2999,
        "benchmark": 92,
        "trust": 95,
        "accuracy": 94,
        "latency": 390,
        "deployments": 6780,
        "reviews": 502,
        "rating": 4.8,
        "verified": True
    }
]

df = pd.DataFrame(models)

current_user = {
    "signed_in": False,
    "name": "Guest",
    "email": ""
}

purchases = []
deployments_list = []
saved_models = []



def get_model(name):
    for model in models:
        if model["name"] == name:
            return model
    return None



def sign_in(email, password):

    if not email or "@" not in email:
        return (
            "Please enter a valid email address.",
            "Status: **Not signed in**"
        )

    name = email.split("@")[0].replace(".", " ").replace("_", " ").title()

    current_user["signed_in"] = True
    current_user["name"] = name
    current_user["email"] = email

    return (
        f"## Welcome, {name}\nYou have successfully signed in to AetherAI.",
        f"Status: **Signed in as {name}**"
    )


def continue_as_guest():

    current_user["signed_in"] = True
    current_user["name"] = "Guest User"
    current_user["email"] = "guest@aetherai.com"

    return (
        "## Welcome, Guest User\nYou are now exploring the AetherAI marketplace.",
        "Status: **Guest User**"
    )



def search_models(search, category, min_trust):

    results = df.copy()

    if search:
        search = str(search).lower()

        results = results[
            results["name"].str.lower().str.contains(search, na=False) |
            results["developer"].str.lower().str.contains(search, na=False) |
            results["description"].str.lower().str.contains(search, na=False)
        ]

    if category != "All":
        results = results[results["category"] == category]

    results = results[results["trust"] >= min_trust]

    display = results[
        [
            "name",
            "developer",
            "category",
            "price",
            "benchmark",
            "trust",
            "accuracy",
            "latency",
            "rating"
        ]
    ].copy()

    display.columns = [
        "Model",
        "Developer",
        "Category",
        "Price (₹)",
        "Benchmark",
        "Trust Score",
        "Accuracy (%)",
        "Latency (ms)",
        "Rating"
    ]

    return display




def show_model_details(name):

    model = get_model(name)

    if not model:
        return "Please select a model."

    verification = "Verified" if model["verified"] else "Pending Verification"

    return f"""
# {model["name"]}

### Model Overview

**Developer:** {model["developer"]}

**Category:** {model["category"]}

**Verification Status:** {verification}

**Community Rating:** {model["rating"]}/5

**Monthly Price:** ₹{model["price"]:,}

---

### About

{model["description"]}

### Performance Snapshot

| Metric | Value |
|---|---:|
| Benchmark Score | {model["benchmark"]}/100 |
| Aether Trust Score | {model["trust"]}/100 |
| Accuracy | {model["accuracy"]}% |
| Latency | {model["latency"]} ms |
| Active Deployments | {model["deployments"]:,} |
| Community Reviews | {model["reviews"]:,} |
"""




def save_model(name):

    if not name:
        return "Please select a model."

    if name not in saved_models:
        saved_models.append(name)
        return f"### {name} saved successfully."

    return f"### {name} is already in your saved models."




def compare_models(selected_models):

    if not selected_models:
        return pd.DataFrame()

    selected_models = selected_models[:3]

    results = df[df["name"].isin(selected_models)].copy()

    display = results[
        [
            "name",
            "price",
            "benchmark",
            "trust",
            "accuracy",
            "latency",
            "rating",
            "deployments"
        ]
    ].copy()

    display.columns = [
        "Model",
        "Price (₹)",
        "Benchmark",
        "Trust Score",
        "Accuracy (%)",
        "Latency (ms)",
        "Rating",
        "Deployments"
    ]

    return display



def trust_explanation(name):

    model = get_model(name)

    if not model:
        return "Please select a model."

    score = model["trust"]

    benchmark_score = round(score * 0.30)
    creator_score = round(score * 0.25)
    reviews_score = round(score * 0.20)
    security_score = round(score * 0.15)

    documentation_score = (
        score
        - benchmark_score
        - creator_score
        - reviews_score
        - security_score
    )

    return f"""
# Aether Trust Score: {score}/100

AetherAI explains why a model is trusted instead of asking users to rely only on marketing claims.

| Verification Factor | Contribution |
|---|---:|
| Benchmark Reliability | {benchmark_score}/30 |
| Creator Verification | {creator_score}/25 |
| Community Reviews | {reviews_score}/20 |
| Security Assessment | {security_score}/15 |
| Documentation Quality | {documentation_score}/10 |

### Why this matters

The Aether Trust Score gives users a transparent way to evaluate AI models before purchasing or deploying them.
"""




def purchase_model(name):

    if not current_user["signed_in"]:
        return "# Sign In Required\nPlease sign in before purchasing a model."

    model = get_model(name)

    if not model:
        return "Please select a valid model."

    already_purchased = any(
        purchase["model"] == model["name"]
        for purchase in purchases
    )

    if already_purchased:
        return f"""
# Already Purchased

You already have access to **{model["name"]}**.

You can now deploy it from the Deploy section.
"""

    platform_fee = round(model["price"] * 0.05)
    total = model["price"] + platform_fee

    purchases.append({
        "id": str(uuid.uuid4()),
        "model": model["name"],
        "amount": total,
        "model_price": model["price"],
        "platform_fee": platform_fee
    })

    return f"""
# Purchase Successful

You now have access to **{model["name"]}**.

| Item | Amount |
|---|---:|
| Model Price | ₹{model["price"]:,} |
| Platform Fee | ₹{platform_fee:,} |
| **Total Paid** | **₹{total:,}** |
"""




def is_purchased(name):

    return any(
        purchase["model"] == name
        for purchase in purchases
    )


def deploy_model(name, deployment_name, region, environment):

    if not current_user["signed_in"]:
        return "# Sign In Required\nPlease sign in before deploying."

    model = get_model(name)

    if not model:
        return "Please select a valid model."

    if not is_purchased(name):
        return f"# Purchase Required\nPlease purchase **{name}** before deploying it."

    if not deployment_name:
        deployment_name = name.lower().replace(" ", "-") + "-deployment"

    endpoint_id = str(uuid.uuid4())[:8]

    endpoint = (
        "https://api.aetherai.demo/v1/"
        + model["id"]
        + "/"
        + endpoint_id
    )

    deployments_list.append({
        "id": str(uuid.uuid4()),
        "name": deployment_name,
        "model": name,
        "region": region,
        "environment": environment,
        "endpoint": endpoint,
        "status": "Active"
    })

    return f"""
# Deployment Successful

Your model is now active.

| Setting | Value |
|---|---|
| Deployment | {deployment_name} |
| Model | {name} |
| Region | {region} |
| Environment | {environment} |
| Status | Active |

### Demo API Endpoint

`{endpoint}`
"""



def dashboard_data():

    total_spend = sum(
        purchase["amount"]
        for purchase in purchases
    )

    stats = f"""
# {current_user["name"]}'s Dashboard

| Metric | Value |
|---|---:|
| Active Deployments | {len(deployments_list)} |
| Models Purchased | {len(purchases)} |
| Saved Models | {len(saved_models)} |
| Total Spend | ₹{total_spend:,.0f} |
| Average Marketplace Trust Score | {df["trust"].mean():.1f}/100 |
"""

    if purchases:

        purchase_df = pd.DataFrame(purchases)

        spending_data = (
            purchase_df
            .groupby("model", as_index=False)["amount"]
            .sum()
        )

    else:

        spending_data = pd.DataFrame({
            "model": [
                "AetherGPT Pro",
                "VisionForge CV",
                "MedInsight AI"
            ],
            "amount": [
                2499,
                1899,
                3999
            ]
        })

    spending_chart = px.bar(
        spending_data,
        x="model",
        y="amount",
        title="Model Spending Overview",
        labels={
            "model": "AI Model",
            "amount": "Amount (₹)"
        }
    )

    activity_df = pd.DataFrame({
        "Metric": [
            "Deployments",
            "Purchases",
            "Saved Models"
        ],
        "Count": [
            len(deployments_list),
            len(purchases),
            len(saved_models)
        ]
    })

    activity_chart = px.bar(
        activity_df,
        x="Metric",
        y="Count",
        title="AetherAI Activity"
    )

    spending_chart.update_layout(template="plotly_white")
    activity_chart.update_layout(template="plotly_white")

    return stats, spending_chart, activity_chart




def publish_model(
    name,
    developer,
    category,
    description,
    price,
    accuracy,
    latency,
    benchmark
):

    if not name or not developer or not description:
        return "# Missing Information\nPlease enter the model name, developer name and description."

    global df

    new_model = {
        "id": name.lower().replace(" ", "-"),
        "name": name,
        "developer": developer,
        "category": category,
        "description": description,
        "price": int(price),
        "benchmark": int(benchmark),
        "trust": 85,
        "accuracy": int(accuracy),
        "latency": int(latency),
        "deployments": 0,
        "reviews": 0,
        "rating": 0,
        "verified": False
    }

    models.append(new_model)
    df = pd.DataFrame(models)

    return f"""
# Model Published Successfully

**{name}** has been added to the AetherAI marketplace.

### Initial Status

- Initial Aether Trust Score: **85/100**
- Verification: **Pending**
- Monetization: **Enabled**
"""




def aether_ai_assistant(message, history):

    # Make history a normal list
    if history is None:
        history = []

    message = str(message or "").strip()

    # Do nothing for empty messages
    if message == "":
        return history, ""

    user_message = message.lower()

    # Default response
    reply = (
        "I can help you discover AI models, compare pricing, check "
        "Trust Scores, evaluate performance, and understand purchasing "
        "or deployment."
    )

    # HEALTHCARE
    if any(word in user_message for word in [
        "health", "medical", "hospital", "clinical"
    ]):
        reply = (
            "For healthcare-related use cases, I recommend MedInsight AI. "
            "It has an Aether Trust Score of 98/100 and an accuracy of 97%."
        )

    # IMAGE
    elif any(word in user_message for word in [
        "image", "picture", "creative", "design"
    ]):
        reply = (
            "For image generation and creative workflows, I recommend "
            "PixelCraft. It costs ₹1,299 per month."
        )

    # SPEECH
    elif any(word in user_message for word in [
        "speech", "voice", "audio"
    ]):
        reply = (
            "For speech and audio applications, I recommend BharatSpeech. "
            "It is optimized for multilingual and Indian language workflows."
        )

    # FINANCE
    elif any(word in user_message for word in [
        "finance", "financial", "forecast"
    ]):
        reply = (
            "For financial analysis and forecasting, I recommend FinSight AI. "
            "It has a Trust Score of 95/100 and an accuracy of 94%."
        )

    # CHEAPEST
    elif any(word in user_message for word in [
        "cheap", "cheapest", "affordable", "budget"
    ]):
        reply = (
            "The most affordable model is PixelCraft at ₹1,299 per month. "
            "BharatSpeech is next at ₹1,499 per month."
        )

    # PRICE
    elif any(word in user_message for word in [
        "price", "cost", "pricing", "how much"
    ]):
        reply = (
            "Current pricing: PixelCraft ₹1,299, BharatSpeech ₹1,499, "
            "VisionForge CV ₹1,899, AetherGPT Pro ₹2,499, "
            "FinSight AI ₹2,999, and MedInsight AI ₹3,999 per month."
        )

    # TRUST
    elif any(word in user_message for word in [
        "trust", "reliable", "safe", "verification"
    ]):
        reply = (
            "MedInsight AI has the highest Aether Trust Score at 98/100. "
            "The score considers benchmarks, creator verification, "
            "community reviews, security and documentation."
        )

    # ACCURACY
    elif any(word in user_message for word in [
        "accuracy", "accurate", "performance", "benchmark"
    ]):
        reply = (
            "MedInsight AI has the highest accuracy at 97%. "
            "VisionForge CV follows with 96% accuracy."
        )

    # MODELS
    elif any(word in user_message for word in [
        "models", "available", "list"
    ]):
        reply = (
            "Available models are AetherGPT Pro, VisionForge CV, "
            "MedInsight AI, BharatSpeech, PixelCraft and FinSight AI."
        )

    # PURCHASE
    elif any(word in user_message for word in [
        "buy", "purchase", "payment"
    ]):
        reply = (
            "Go to the Purchase tab, select a model and click "
            "Buy Model Access. Once purchased, you can deploy it."
        )

    # DEPLOY
    elif any(word in user_message for word in [
        "deploy", "deployment", "api", "endpoint"
    ]):
        reply = (
            "First purchase the model. Then open the Deploy tab, "
            "select the model, enter a deployment name, choose a region "
            "and environment, then click Deploy Model."
        )

    # CREATOR
    elif any(word in user_message for word in [
        "sell", "creator", "publish", "monetize",
        "monetise", "upload"
    ]):
        reply = (
            "Use Creator Studio to publish and monetize your AI model. "
            "Add the model details, price and performance metrics, "
            "then click Publish Model."
        )

    # GREETING
    elif any(word in user_message for word in [
        "hello", "hi", "hey"
    ]):
        reply = (
            "Hello. I am the AetherAI Assistant. Ask me about AI models, "
            "pricing, Trust Scores, performance or deployment."
        )

    # Add the conversation using a simple list
    new_history = list(history)
    new_history.append([message, reply])

    return new_history, ""


print("AetherAI backend loaded successfully.")


custom_css = """

:root {
    color-scheme: dark !important;
    --bg: #08090d;
    --surface: #0f1118;
    --surface-2: #151822;
    --surface-3: #1a1e2a;
    --border: rgba(255,255,255,0.09);
    --border-strong: rgba(255,255,255,0.15);
    --text: #f5f7fb;
    --muted: #9299aa;
    --accent: #8b7cff;
    --accent-2: #b19cff;
    --success: #35d39a;
}

/* Global */
html, body, .gradio-container {
    background:
        radial-gradient(circle at 85% 5%, rgba(139,124,255,0.10), transparent 28%),
        radial-gradient(circle at 5% 25%, rgba(74,222,222,0.055), transparent 25%),
        #08090d !important;
    color: var(--text) !important;
    font-family: "DM Sans", sans-serif !important;
}

.gradio-container {
    max-width: 1480px !important;
    margin: auto !important;
    padding: 28px 34px 50px !important;
}

footer { display: none !important; }

/* Typography */
h1, h2, h3, h4, p, label, span {
    color: var(--text) !important;
}

h1 {
    letter-spacing: -0.035em !important;
    font-weight: 800 !important;
}

h2 {
    letter-spacing: -0.02em !important;
    font-weight: 750 !important;
}

.prose p, .prose li {
    color: #aeb4c3 !important;
    line-height: 1.7 !important;
}

/* Hero / brand panels */
.hero {
    background:
        linear-gradient(135deg, rgba(139,124,255,0.18), rgba(17,19,27,0.78) 55%, rgba(53,211,154,0.05)),
        #0e1017 !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 22px !important;
    padding: 34px 38px !important;
    margin: 8px 0 26px !important;
    box-shadow: 0 18px 55px rgba(0,0,0,0.28) !important;
}

.hero h1 {
    font-size: 42px !important;
    margin-bottom: 6px !important;
}

.hero h2, .hero h3 {
    color: #c9c2ff !important;
}

/* Containers */
.gr-block,
.gr-box,
.gr-panel,
.gr-group,
.gr-form {
    background: rgba(15,17,24,0.88) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 16px !important;
}

.gr-group, .gr-form {
    box-shadow: 0 8px 30px rgba(0,0,0,0.16) !important;
}

/* Inputs */
input, textarea, select,
.gr-input, .wrap {
    background: #0b0d12 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
}

input:focus, textarea:focus {
    border-color: rgba(139,124,255,0.7) !important;
    box-shadow: 0 0 0 3px rgba(139,124,255,0.10) !important;
}

/* Dropdowns / sliders */
.dropdown, .wrap.svelte-1ipelgc {
    background: #0b0d12 !important;
}

input::placeholder, textarea::placeholder {
    color: #646b7a !important;
}

/* Buttons */
button {
    border-radius: 11px !important;
    border: 1px solid var(--border) !important;
    font-weight: 650 !important;
    transition: all 0.18s ease !important;
}

button:hover {
    transform: translateY(-1px) !important;
    border-color: rgba(139,124,255,0.45) !important;
}

button.primary {
    background: linear-gradient(135deg, #8b7cff, #6f62e8) !important;
    border-color: transparent !important;
    box-shadow: 0 8px 24px rgba(111,98,232,0.22) !important;
}

button.primary:hover {
    box-shadow: 0 12px 30px rgba(111,98,232,0.34) !important;
}

/* Tabs */
.tab-nav {
    background: #0c0e14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    margin-bottom: 22px !important;
}

.tab-nav button {
    background: transparent !important;
    color: #8e95a5 !important;
    border: 0 !important;
    border-radius: 10px !important;
}

.tab-nav button.selected {
    background: #1a1d27 !important;
    color: #ffffff !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06) !important;
}

/* Data tables */
table {
    background: #0d0f15 !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

th {
    background: #151822 !important;
    color: #bfc5d3 !important;
    border-color: var(--border) !important;
}

td {
    background: #0d0f15 !important;
    color: #e5e8ef !important;
    border-color: rgba(255,255,255,0.055) !important;
}

/* Markdown output cards */
.prose {
    color: var(--text) !important;
}

.prose table {
    border-radius: 12px !important;
    overflow: hidden !important;
}

.prose code {
    background: #080a0f !important;
    color: #c7c0ff !important;
    border: 1px solid var(--border) !important;
    padding: 3px 7px !important;
    border-radius: 6px !important;
}

/* Plot containers */
.plot-container, .gradio-plot {
    background: #0f1118 !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* Subtle separation for rows */
.gr-row {
    gap: 16px !important;
}

/* Login screen breathing room */
#component-0 {
    min-height: 100vh !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #08090d;
}
::-webkit-scrollbar-thumb {
    background: #292d39;
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3a3f4e;
}
"""

def login_and_open(email, password):

    message, status = sign_in(email, password)

    return (
        gr.update(visible=False),
        gr.update(visible=True),
        status,
        message
    )


def guest_and_open():

    message, status = continue_as_guest()

    return (
        gr.update(visible=False),
        gr.update(visible=True),
        status,
        message
    )


with gr.Blocks(
    title="AetherAI",
    fill_width=True
) as app:


    with gr.Column(
        visible=True
    ) as login_screen:

        gr.Markdown("""
        <div class="hero">
        <h1>AetherAI</h1>
        <h3>Trusted AI Model Marketplace</h3>
        <p>Discover. Compare. Verify. Purchase. Deploy.</p>
        </div>
        """)

        with gr.Row():

            with gr.Column(scale=1):

                gr.Markdown("## Sign in to continue")

                login_email = gr.Textbox(
                    label="Email Address",
                    placeholder="you@example.com"
                )

                login_password = gr.Textbox(
                    label="Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = gr.Button(
                    "Sign In",
                    variant="primary"
                )

                guest_button = gr.Button(
                    "Continue as Guest"
                )

                login_message = gr.Markdown()

            with gr.Column(scale=1):

                gr.Markdown("""
                ## Why AetherAI?

                **Discover AI Models**  
                Find AI models based on capability and use case.

                **Compare Transparently**  
                Evaluate pricing, benchmarks, accuracy and latency.

                **Verify Trust**  
                Understand the evidence behind every Trust Score.

                **Deploy Easily**  
                Move from discovery to deployment through one platform.

                **Monetize Your Work**  
                AI creators can publish and sell their models.
                """)



    with gr.Column(
        visible=False
    ) as main_app:

        with gr.Row():

            with gr.Column(scale=4):

                gr.Markdown("""
                # AetherAI
                ### Trusted AI Model Marketplace
                """)

            with gr.Column(scale=1):

                user_status = gr.Markdown(
                    "Status: **Signed in**"
                )

        gr.Markdown("""
        <div class="hero">
        <h2>Discover the right AI. Know why you can trust it.</h2>
        <p>
        Compare AI models, evaluate transparent benchmarks,
        purchase access and deploy through one accessible platform.
        </p>
        </div>
        """)


        with gr.Tabs():


            with gr.Tab("Marketplace"):

                gr.Markdown("# AI Model Marketplace")

                with gr.Row():

                    search_input = gr.Textbox(
                        label="Search",
                        placeholder="Search models or developers"
                    )

                    category_filter = gr.Dropdown(
                        choices=[
                            "All",
                            "Large Language Models",
                            "Computer Vision",
                            "Healthcare AI",
                            "Speech and Audio",
                            "Image Generation",
                            "Finance AI"
                        ],
                        value="All",
                        label="Category"
                    )

                    trust_filter = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=1,
                        label="Minimum Trust Score"
                    )

                search_button = gr.Button(
                    "Search Models",
                    variant="primary"
                )

                marketplace_table = gr.Dataframe(
                    value=search_models("", "All", 0),
                    interactive=False,
                    label="Available AI Models"
                )

                search_button.click(
                    search_models,
                    inputs=[
                        search_input,
                        category_filter,
                        trust_filter
                    ],
                    outputs=marketplace_table
                )

                gr.Markdown("## Model Details")

                marketplace_model_selector = gr.Dropdown(
                    choices=[
                        model["name"]
                        for model in models
                    ],
                    label="Select a Model"
                )

                with gr.Row():

                    details_button = gr.Button(
                        "View Details",
                        variant="primary"
                    )

                    save_button = gr.Button(
                        "Save Model"
                    )

                model_details_output = gr.Markdown()
                save_output = gr.Markdown()

                details_button.click(
                    show_model_details,
                    inputs=marketplace_model_selector,
                    outputs=model_details_output
                )

                save_button.click(
                    save_model,
                    inputs=marketplace_model_selector,
                    outputs=save_output
                )


            with gr.Tab("Compare Models"):

                gr.Markdown("# Compare AI Models")

                compare_selector = gr.Dropdown(
                    choices=[
                        model["name"]
                        for model in models
                    ],
                    multiselect=True,
                    label="Select up to 3 Models"
                )

                compare_button = gr.Button(
                    "Compare Models",
                    variant="primary"
                )

                compare_output = gr.Dataframe(
                    interactive=False,
                    label="Comparison Results"
                )

                compare_button.click(
                    compare_models,
                    inputs=compare_selector,
                    outputs=compare_output
                )



            with gr.Tab("Trust & Verification"):

                gr.Markdown("# Aether Trust Score")

                trust_selector = gr.Dropdown(
                    choices=[
                        model["name"]
                        for model in models
                    ],
                    label="Select a Model"
                )

                trust_button = gr.Button(
                    "View Trust Breakdown",
                    variant="primary"
                )

                trust_output = gr.Markdown()

                trust_button.click(
                    trust_explanation,
                    inputs=trust_selector,
                    outputs=trust_output
                )


            with gr.Tab("Purchase"):

                gr.Markdown("""
                # Purchase Model Access

                Transparent pricing in Indian Rupees.
                """)

                purchase_selector = gr.Dropdown(
                    choices=[
                        model["name"]
                        for model in models
                    ],
                    label="Select a Model"
                )

                purchase_button = gr.Button(
                    "Buy Model Access",
                    variant="primary"
                )

                purchase_output = gr.Markdown()

                purchase_button.click(
                    purchase_model,
                    inputs=purchase_selector,
                    outputs=purchase_output
                )


    

            with gr.Tab("Deploy"):

                gr.Markdown("# One-Click Deployment")

                deploy_selector = gr.Dropdown(
                    choices=[
                        model["name"]
                        for model in models
                    ],
                    label="Select Model"
                )

                deployment_name_input = gr.Textbox(
                    label="Deployment Name",
                    placeholder="My Production AI"
                )

                with gr.Row():

                    region_input = gr.Dropdown(
                        choices=[
                            "Mumbai",
                            "Bengaluru",
                            "Delhi",
                            "Singapore"
                        ],
                        value="Bengaluru",
                        label="Deployment Region"
                    )

                    environment_input = gr.Dropdown(
                        choices=[
                            "Development",
                            "Testing",
                            "Production"
                        ],
                        value="Production",
                        label="Environment"
                    )

                deploy_button = gr.Button(
                    "Deploy Model",
                    variant="primary"
                )

                deploy_output = gr.Markdown()

                deploy_button.click(
                    deploy_model,
                    inputs=[
                        deploy_selector,
                        deployment_name_input,
                        region_input,
                        environment_input
                    ],
                    outputs=deploy_output
                )


        

            with gr.Tab("Dashboard"):

                gr.Markdown("# Your AetherAI Dashboard")

                dashboard_button = gr.Button(
                    "Refresh Dashboard",
                    variant="primary"
                )

                dashboard_stats = gr.Markdown()

                with gr.Row():

                    spending_chart = gr.Plot(
                        label="Spending Overview"
                    )

                    activity_chart = gr.Plot(
                        label="Marketplace Activity"
                    )

                dashboard_button.click(
                    dashboard_data,
                    outputs=[
                        dashboard_stats,
                        spending_chart,
                        activity_chart
                    ]
                )


        

            with gr.Tab("Creator Studio"):

                gr.Markdown("""
                # Creator Studio

                Publish and monetize your AI model.
                """)

                with gr.Row():

                    creator_model_name = gr.Textbox(
                        label="Model Name"
                    )

                    creator_name = gr.Textbox(
                        label="Creator / Developer"
                    )

                creator_category = gr.Dropdown(
                    choices=[
                        "Large Language Models",
                        "Computer Vision",
                        "Healthcare AI",
                        "Speech and Audio",
                        "Image Generation",
                        "Finance AI"
                    ],
                    value="Large Language Models",
                    label="Category"
                )

                creator_description = gr.Textbox(
                    label="Model Description",
                    lines=4
                )

                with gr.Row():

                    creator_price = gr.Number(
                        label="Monthly Price (₹)",
                        value=999
                    )

                    creator_accuracy = gr.Number(
                        label="Accuracy (%)",
                        value=90
                    )

                with gr.Row():

                    creator_latency = gr.Number(
                        label="Latency (ms)",
                        value=300
                    )

                    creator_benchmark = gr.Number(
                        label="Benchmark Score",
                        value=85
                    )

                publish_button = gr.Button(
                    "Publish Model",
                    variant="primary"
                )

                publish_result = gr.Markdown()

                publish_button.click(
                    publish_model,
                    inputs=[
                        creator_model_name,
                        creator_name,
                        creator_category,
                        creator_description,
                        creator_price,
                        creator_accuracy,
                        creator_latency,
                        creator_benchmark
                    ],
                    outputs=publish_result
                )


    

        chat_open_button = gr.Button(
            "AI",
            elem_classes="floating-chat-button"
        )

        with gr.Column(
            visible=False,
            elem_classes="chat-window"
        ) as floating_chat:

            with gr.Row():

                with gr.Column(scale=4):

                    gr.Markdown(
                        "### AetherAI Assistant"
                    )

                with gr.Column(scale=1):

                    chat_close_button = gr.Button(
                        "Close"
                    )

            floating_chatbot = gr.Chatbot(
                height=350,
                label="AetherAI Assistant",
                value=[]
            )

            floating_chat_input = gr.Textbox(
                placeholder="Ask about AI models...",
                show_label=False
            )

            floating_chat_send = gr.Button(
                "Send",
                variant="primary"
            )


        chat_open_button.click(
            lambda: gr.update(visible=True),
            outputs=floating_chat
        )

        chat_close_button.click(
            lambda: gr.update(visible=False),
            outputs=floating_chat
        )

        floating_chat_send.click(
            aether_ai_assistant,
            inputs=[
                floating_chat_input,
                floating_chatbot
            ],
            outputs=[
                floating_chatbot,
                floating_chat_input
            ]
        )

        floating_chat_input.submit(
            aether_ai_assistant,
            inputs=[
                floating_chat_input,
                floating_chatbot
            ],
            outputs=[
                floating_chatbot,
                floating_chat_input
            ]
        )




    login_button.click(
        login_and_open,
        inputs=[
            login_email,
            login_password
        ],
        outputs=[
            login_screen,
            main_app,
            user_status,
            login_message
        ]
    )

    guest_button.click(
        guest_and_open,
        outputs=[
            login_screen,
            main_app,
            user_status,
            login_message
        ]
    )


print("AetherAI UI with floating chatbot loaded successfully.")
