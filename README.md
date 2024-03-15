init locales
:$find . -type f -name '*.py' -not -path "./venv/*" | xargs pybabel extract -o locales/messages.pot
