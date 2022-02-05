# shopping_list_plugin

Das ShoppingList-Plugin fügt neue Seiten hinzu, auf der man Einkaufslisten mit Produkten verwalten kann.
Des Weiteren kann man als Admin Einheiten für die Produkte verwalten.

## Init
Dieses Repo wird in den plugins-Ordner des Servers geklont
```shell
cd py_api/plugins/
git clone "this repo"
```

Dann muss der Server einmal neu gestartet werden, um die Datenbank-Struktur zu erstellen.

Im Anschluss kann die write_shopping_list_plugin_data.py ausgeführt werden, um die Datenbank mit Anfangswerten zu bestatten.
