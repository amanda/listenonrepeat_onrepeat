drop table if exists videos;
create table videos (
	ytid text primary key not null,
	title text not null,
	plays integer default 0 not null 
);
