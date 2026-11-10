#!/bin/sh
set -e

echo "[CHECK] Проверка базы данных events.db..."
if [ ! -f /dbdata/events.db ]; then
    echo "Ошибка: events.db не найден!"
    exit 1
fi

res_events=$(sqlite3 /dbdata/events.db "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='events';")
res_regs=$(sqlite3 /dbdata/events.db "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='registrations';")

if [ "$res_events" -eq 1 ] && [ "$res_regs" -eq 1 ]; then
    echo "Таблицы 'events' и 'registrations' успешно проверены."
else
    echo "Ошибка: таблицы в events.db повреждены или отсутствуют!"
    exit 1
fi

echo "[CHECK] Проверка базы данных admins.db..."
if [ ! -f /dbdata/admins.db ]; then
    echo "Ошибка: admins.db не найден!"
    exit 1
fi

res_admins=$(sqlite3 /dbdata/admins.db "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='admins';")
if [ "$res_admins" -eq 1 ]; then
    echo "Таблица 'admins' найдена."
else
    echo "Ошибка: таблица 'admins' отсутствует!"
    exit 1
fi

echo "[OK] Все базы данных валидны. Выход."
exit 0
