# Corona Navigator

## Info
Für das Modul WOWEB/WODSS wurde ein Corona Navigator erstellt. Ziel der Arbeit war es, einen Kantonsservice, ein Backend und ein Frontend zu erstellen. Der Kantonssevice dient dazu, Daten für einen bestimmten Kanton zu erhalten. Für unsere Gruppe war das die beiden Halbkantone Ba-sel-Land und Basel-Stadt.
Mit dem Backend sollen nun die anderen 11 Kantonsservices angefragt werden und die Daten in ei-ner Speicherstruktur gespeichert werden. Diese Daten werden bei uns in einer MongoDB gespei-chert und dem Frontend zur Verfügung gestellt.
Am Ende der Arbeit ist ein Navigator entstanden, der für Zugstrecken die Inzidenz der jeweiligen Gemeinden der Zwischenstationen anzeigt. Die Navigation mit dem Auto, gibt jeweils die Inzidenz vom Start- und Endpunkt sowie einer Zwischenstation aus. Ausserdem haben wir eine Statusseite eingebaut, die die Inzidenz farblich auf einer Karte darstellt, sowie die Daten, die in der Datenbank gespeichert sind, anzeigt.
Die fertige Lösung kann per folgender URL zugegriffen werden:

<img src="https://github.com/dev-ale/corona-navigator-woweb/blob/master/images_repo/screenshot_train.jpg?raw=true" width="500" alt="screenshot_car">
<img src="https://github.com/dev-ale/corona-navigator-woweb/blob/master/images_repo/screenshot_car.jpg?raw=true" width="500" alt="screenshot_car">
<img src="https://github.com/dev-ale/corona-navigator-woweb/blob/master/images_repo/screenshot_status.jpg?raw=true" width="500" alt="screenshot_car">

## Live
https://corona-navigator.herokuapp.com/

## Run

### Run Locally
#### Install Python Modules
Run
```pip install -r requirements.txt```
#### Start Server
Run
```python app.py```
#### Start Frontend (no Server needed locally)
Run <br>
```yarn install```<br>

```yarn serve```
#### Start Local Database
Run <br>
```export MONGO_URI="mongodb://localhost:27017/serviceDB"```<br>

```make database```

### Build Frontend
```yarn build```

### Deploy
* push to master
