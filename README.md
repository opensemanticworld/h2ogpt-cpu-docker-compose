# h2ogpt-cpu-docker-compose

Default model https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin (~7GB) will be downloaded on first run

## Configuration

### Caddy reverse proxy

docker-compose.override.yml
```yml
version: "3.8"
services:
  h2ogpt:
    networks:
      - caddy
    labels:
      caddy: ${H2OGPT_SERVER}
      caddy.reverse_proxy: "{{upstreams 7860}}"
      caddy.basicauth: "* bcrypt"
      caddy.basicauth.admin: "${BASICAUTH_HASHED_PASSWORD}"

networks:
  # Add caddy as an external network.
  caddy:
    external: true
```

### Chat only

docker-compose.override.yml
```yml
version: "3.8"
services:
  h2ogpt:
    entrypoint: [
      "conda", "run", "--no-capture-output", "-n", "h2ogpt", 
      "python", "h2ogpt/generate.py", 
      "--base_model='llama'", 
      "--prompt_type=llama2", 
      "--score_model=None", 
      "--langchain_mode='UserData'", 
      "--user_path=userdata",
      "--detect_user_path_changes_every_query=True",
      "--visible_submit_buttons=False",
      "--visible_side_bar=False",
      "--visible_submit_buttons=False",
      "--visible_side_bar=False",
      "--visible_chat_tab=True", 
      "--visible_doc_selection_tab=False", 
      "--visible_doc_view_tab=False", 
      "--visible_chat_history_tab=False", 
      "--visible_expert_tab=False", 
      "--visible_models_tab=False", 
      "--visible_system_tab=False", 
      "--visible_tos_tab=False", 
      "--visible_hosts_tab=False", 
      "--chat_tables=True",
      "--visible_h2ogpt_header=False"
    ]
```

## Usage

### Scrape wiki pages
```bash
docker compose exec h2ogpt conda run -n h2ogpt python /app/scrape.py
```

## Known problems
Container randomly crashes (and restarts) due to a segmentation fault