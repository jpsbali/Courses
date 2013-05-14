select count(a.docid) from frequency a, frequency b where a.docid=b.docid and a.term='transactions' and b.term='world';
