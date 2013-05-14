select count(*) from (select docid from frequency where docid in (select distinct(docid) from frequency) group by docid having SUM(count) > 300);
