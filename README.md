init locales
:$find . -type f -name '*.py' -not -path "./venv/*" | xargs pybabel extract -o locales/messages.pot

add locale
:$pybabel init -i locales/messages.pot -d locales -D tg_bot_for_ag -l {locale}

compile locales
:$pybabel compile -d locales -D tg_bot_for_ag