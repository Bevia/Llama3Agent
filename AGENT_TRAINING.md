# Agent Training Guide

In your current setup, you're not really "training" anything — you're just querying a pre-trained Llama 3 model. "Training" your agent can mean different things depending on your goal:

---

## Option 1: Fine-tuning (actual training on your data)

You'd train a custom version of Llama 3 on your own dataset, then load it via Ollama.

**Tools:** [Unsloth](https://github.com/unslothai/unsloth) or [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) — both support Llama 3 and are relatively low-resource.

**Steps (high level):**
1. Prepare a dataset in JSONL format (`{"prompt": "...", "response": "..."}`)
2. Fine-tune using one of the tools above
3. Export the model to GGUF format
4. Import it into Ollama: `ollama create my-model -f Modelfile`
5. Change `"llama3"` → `"my-model"` in `llamaAgent.py`

Best for: making the model answer like a specific persona, follow a domain style, or know specific facts consistently.

---

## Option 2: System Prompt (easiest, no training)

Add a system message to `llamaAgent.py` to give the model a role or behavior. This is the quickest way to "shape" the agent.

Change `llamaAgent.py` from:
```python
messages=[{"role": "user", "content": user_text}]
```
to:
```python
messages=[
    {"role": "system", "content": "You are a helpful assistant specialized in Python development. Be concise and technical."},
    {"role": "user", "content": user_text}
]
```

Best for: personality, tone, domain focus, response format.

---

## Option 3: RAG — feed it your own documents (no training)

Add a retrieval step that pulls relevant text from your own files/docs and injects it into the prompt before sending to Ollama.

**Tools:** [LlamaIndex](https://www.llamaindex.ai/) or [LangChain](https://python.langchain.com/)

Best for: making the model answer questions about your own codebase, documents, or knowledge base without retraining.

---

## Option 4: Conversation Memory (multi-turn context)

Your agent currently has no memory between queries. Adding a `history` list makes it feel "trained" on the conversation:

```python
history = []

def ask(user_text):
    history.append({"role": "user", "content": user_text})
    response = ollama.chat(model="llama3", messages=history)
    reply = response["message"]["content"]
    history.append({"role": "assistant", "content": reply})
    return reply
```

Best for: coherent multi-turn conversations.

---

## Which one fits your goal?

| Goal | Best approach |
|---|---|
| Custom personality / domain behavior | System prompt (Option 2) |
| Answer questions about your own docs | RAG (Option 3) |
| Remember previous messages | Conversation memory (Option 4) |
| Deep behavioral change / specialized knowledge | Fine-tuning (Option 1) |

The easiest meaningful improvement is **Option 2** (system prompt) — it's a 3-line change.

---

## Upgrading the Model Version

When switching to a newer Llama model, you must pull it via Ollama before running the app — otherwise it will fail silently.

**Steps:**
1. Pull the new model:
   ```bash
   ollama pull llama3.2
   ```
2. Update the model name in `llamaAgent.py`:
   ```python
   response = ollama.chat(model="llama3.2", messages=[...])
   ```
3. Verify installed models anytime with:
   ```bash
   ollama list
   ```

> **Note:** `llama3.2` is ~2GB. The app will not work until the download completes.
