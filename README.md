# ObsidianGPT

As opposed to many existing projects that aim to integrate OpenAI's GPT-X with Obsidian, this project integrates vour Obsidian vault into ChatGPT. This has the advantage of keeping access to all your beloved ChatGPT features like Browsing, custom GPTs and voice control(if you use the mobile app).

## Who is this for?
If you like to brainstorm, do research, make plans or write with ChatGPT, this setup is for you. It let's you:
- Summarize a conversation into beautifully Obsidian-flavoured markdown. 
- Create a new note in your vault.
- Append to an existing note.

Potential future features could include:
- Editing notes.
- Usage of templates.
- Searching your vault.

Besides liking to work in ChatGPT, you need a setup where you have your vault stored at some place that you can mount into a docker container. Furthermore you need to be able proxy to the container from a public domain. You can find out about an example setup [over here](). This setup uses a cheap VPN as an always-on copy of an Obsidian vault, but I am sure serverless solutions with could work as well.

## How to set it up
To be able to integrate your Obsidian vault with ChatGPT, you need your vault on some kind of machine that has [Docker](https://www.docker.com) installed and that you can access with via a public domain. To be able to upgrade easily, I recommend the following set up:

1. Basic setup:
´mkdir -p /wherever/whatever` as the root for your project.
´cd /wherever/whatever´
´git clone https://github.com/kon-foo/ObsidianGPT.git`
2. Copy necessary files out of the repository:
`cp ObsidianGPT/backend/.env.template .env && cp ObsidianGPT/backend/docker-compose.yml . && cp ObsidianGPT/upgrade.sh . && cp ObsidianGPT/logs.sh . && cp ObsidianGPT/set-api-key.sh .`
`chmod +x upgrade.sh logs.sh set-api-key.sh`
3. Set environment variables:
`./set-api-key.sh` to generate a key and set it in the .env file.
You may also want to set the following variable in the .env file:
- `DOMAIN` your public domain
- `IGNORE_DIRS` a comma separated list of directories that you want to ignore when using the list notes endpoint. For example your templates directory.
4. Edit the docker-compose.yml file:
- Mount your vault to `/app/vault`.
5. Start the container:
`docker-compose up --build -d`

### Upgrading the backend
To upgrade, simply run `./upgrade.sh` in the root of your project. This will pull the latest version of the backend and rebuild the docker image.

### Creating you custom GPT
1. Head over to [ChatGPT](https://chat.openai.com/) and create a new GPT. 
2. Click on "Create new action".
3. For the authentication chose type "API Key" and auth type "custom". As the Custom Header Name, use "X-API-KEY" and as the API Key, use the key you have in the .env file.
4. Head over to yourdomain.com/docs, Open the "schema" endpoint, click on "Try it out", enter your API key and click "Execute". Copy the schema and paste it into the "schema" field in the "Create new action" form.
5. Copy the ObsidianGPT/prompt.md file into the "prompt" field. Note: The prompt works, but I haven't thoroughly tested and optimized it. Feel free to suggest improvements.
6. Publish to "Only me".

## How to use:
Pin the GPT or at least use it once directly to make it accessible via @mentions. Then in your next interesting ChatGPT conversation, just type: `@ObsidianGPT summarize the key points of this conversations and add it to my XYZ note` 