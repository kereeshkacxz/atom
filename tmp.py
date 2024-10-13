curl https://api.proxyapi.ru/anthropic/v1/messages \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer sk-ks9n4SXZvduNF5N9JTLjRzloDrewssKJ" \
    -H "Anthropic-Version: 2023-06-01" \
    -d '{
        "model": "claude-3-opus-20240229",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "max_tokens": 1024
    }'