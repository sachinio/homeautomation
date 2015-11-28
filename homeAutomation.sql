drop table if exists settings;
create table settings (
  id integer primary key autoincrement,
  name text not null,
  value text not null
);