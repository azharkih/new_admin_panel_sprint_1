# Greetings traveller

Мы рады, что вы приступили к выполнению 1 задания из курса Middle Python-разработчик.
 
Описание структуры и порядок выполнения проекта:
1. `schema_design` - раздел c материалами для архитектуры базы данных.
2. `movies_admin` - раздел с материалами для панели администратора.
3. `sqlite_to_postgres` - раздел с материалами по миграции данных.

Напоминаем, что все три части работы нужно сдавать на ревью одновременно.

Успехов!

psql -h 127.0.0.1 -U app -d movies_database
    SHOW search_path; 
    SET search_path TO content,public; 

psql -h 127.0.0.1 -U app -d movies_database -f movies_database.ddl 