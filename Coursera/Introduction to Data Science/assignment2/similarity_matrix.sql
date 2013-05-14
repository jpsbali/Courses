select SUM(total) from (select a.count*b.count total from frequency a, frequency b where a.docid='10080_txt_crude' and b.docid='17035_txt_earn' and a.term=b.term group by a.term,b.term);

select a.docid, b.docid, SUM(a.count*b.count) from frequency a, frequency b where a.term=b.term and a.docid='10080_txt_crude' and b.docid='17035_txt_earn' group by a.docid, b.docid; 

