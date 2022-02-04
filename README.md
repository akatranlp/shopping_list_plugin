# shopping_list_plugin

Das ShoppingList-Plugin fügt eine neue Seite hinzu, auf der man eine Einkauflsite mit Produkten verwalten kann

## Init
Dieses Repo wird in den plugins Ordner des Servers geklont
```shell
cd py_api/plugins/
git clone "this repo"
```

Dann muss der Server einmal neugestartet werden, um die Datenbank-Struktur zu erstellen.

Im anschluss muss die write_shopping_list_plugin_data.py ausgeführt werden, um die db
mit Anfangswerten zu bestatten.
