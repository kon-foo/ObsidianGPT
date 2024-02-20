# ObsidianGPT

As opposed to many existing projects that aim to integrate OpenAI's GPT-X with Obsidian, this project integrates vour Obsidian vault into ChatGPT. This has the advantage of keeping access to all your beloved ChatGPT features like Browsing, custom GPTs and voice control(if you use the mobile app).

## Who is this for?
This is for people who like to *work* in ChatGPT. If you like to brainstorm, do research, make plans or write with ChatGPT, this setup is for you. It let's you:
- Summarize a conversation into beautifully Obsidian flavoured markdown. 
- Create a new note in your vault.
- Append to an existing note.

In the future, I plan to add more features like:
- Editing notes.
- Usage of your templates.
- Searching your vault.

Besides liking to work in ChatGPT, you need a setup where you have you vault stored at some place that you can mount into a docker container. And be able proxy the traffic to the container from a public domain. In my case, I had a cheap VPS that I used for syncing my vault with Syncthing anyways. So I only had to add a reverse proxy to the setup and point a subdomain to it. But I am sure there are serverless solutions that could work as well.

## How to use
...