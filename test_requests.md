# Примеры запросов к API

## 🌐 Базовый URL
```
http://localhost:8000
```

---

## 1️⃣ Получить все карты
Invoke-RestMethod -Uri "http://localhost:8000/karts" -Method Get

---

## 2️⃣ Создать новый карт

$body = @{
    model = "TurboKart 5000"
    state = $true
    tires = "Medium"
    tires_change_date = "2025-12-10"
    rain = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/karts" -Method Post -Body $body -ContentType "application/json"

---

## 3️⃣ Получить все трассы

Invoke-RestMethod -Uri "http://localhost:8000/tracks" -Method Get

---

## 4️⃣ Создать новую трассу

$body = @{
    name = "Thunder Circuit"
    state = $true
    open = $true
    length = 3.2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tracks" -Method Post -Body $body -ContentType "application/json"

---

## 5️⃣ Создать гонку

$body = @{
    track_id = 1
    race_date = "2025-12-20"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/races" -Method Post -Body $body -ContentType "application/json"

---

## 6️⃣ Получить все гонки на трассе

Invoke-RestMethod -Uri "http://localhost:8000/tracks/1/races" -Method Get

---

## 7️⃣ Создать гонщика

$body = @{
    name = "Max Verstappen"
    club_card = $true
    date_of_birth = "1997-09-30"
    date_of_registration = "2024-01-15"
    best_time = "01:20:00"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/racers" -Method Post -Body $body -ContentType "application/json"

---

## 8️⃣ Записать результат гонки

$body = @{
    race_id = 1
    racer_id = 1
    kart_id = 2
    duration = "01:27:30"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/race-results" -Method Post -Body $body -ContentType "application/json"

---

## 9️⃣ Получить результаты конкретной гонки

Invoke-RestMethod -Uri "http://localhost:8000/races/1/results" -Method Get

---

## 🔟 Получить историю гонщика

Invoke-RestMethod -Uri "http://localhost:8000/racers/1/history" -Method Get

---

## 1️⃣1️⃣ Получить конкретную гонку с информацией о трассе

Invoke-RestMethod -Uri "http://localhost:8000/races/1" -Method Get

