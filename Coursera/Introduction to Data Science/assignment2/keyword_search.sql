insert into frequency values ('q', 'washington', 1);

insert into frequency values ('q', 'taxes', 1);

insert into frequency values ('q', 'treasury', 1);

select docid, count from frequency where docid in (select distinct(docid) from frequency where docid in (select distinct(docid) from frequency where term='washington') and term='taxes') and term='treasury';

select max(s) from (select a.docid as docidA, b.docid as docidB, SUM(a.count*b.count) as s from frequency a, frequency b where a.term=b.term and a.docid='q' group by a.docid, b.docid);

